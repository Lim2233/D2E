"""
文档解析模块
支持 Word/Excel/Markdown/TXT 转换为统一的 JSON 结构
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Union
from dataclasses import dataclass, asdict


@dataclass
class ParsedDocument:
    """解析后的文档数据结构"""
    filename: str
    file_type: str
    content: Union[str, List[Dict], Dict]
    metadata: Dict[str, Any]
    sections: List[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class DocumentParser:
    """文档解析器基类"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.filename = self.file_path.name
        self.file_type = self.file_path.suffix.lower()
    
    def parse(self) -> ParsedDocument:
        """解析文档，子类需要重写此方法"""
        raise NotImplementedError("子类必须实现 parse 方法")
    
    def _get_metadata(self) -> Dict[str, Any]:
        """获取文件元数据"""
        stat = self.file_path.stat()
        return {
            "file_size": stat.st_size,
            "file_path": str(self.file_path),
            "file_extension": self.file_type,
        }


class WordParser(DocumentParser):
    """Word 文档解析器 (.docx)"""
    
    def parse(self) -> ParsedDocument:
        from docx import Document
        
        doc = Document(self.file_path)
        
        # 提取段落
        paragraphs = []
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append({
                    "type": "paragraph",
                    "text": para.text.strip(),
                    "style": para.style.name if para.style else None
                })
        
        # 提取表格
        tables = []
        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                table_data.append(row_data)
            tables.append({
                "type": "table",
                "data": table_data
            })
        
        # 合并所有内容
        sections = paragraphs + tables
        
        # 提取纯文本内容
        full_text = "\n".join([p["text"] for p in paragraphs])
        
        return ParsedDocument(
            filename=self.filename,
            file_type="docx",
            content=full_text,
            metadata=self._get_metadata(),
            sections=sections
        )


class ExcelParser(DocumentParser):
    """Excel 文档解析器 (.xlsx)"""
    
    def parse(self) -> ParsedDocument:
        import pandas as pd
        
        # 读取所有 sheet
        xls = pd.ExcelFile(self.file_path)
        sheets_data = []
        
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            
            # 将 DataFrame 转换为字典列表
            records = df.replace({pd.NaT: None, pd.NA: None}).to_dict('records')
            
            # 清理 NaN 值
            cleaned_records = []
            for record in records:
                cleaned = {k: (v if pd.notna(v) else None) 
                          for k, v in record.items()}
                cleaned_records.append(cleaned)
            
            sheets_data.append({
                "sheet_name": sheet_name,
                "columns": list(df.columns),
                "row_count": len(df),
                "data": cleaned_records
            })
        
        return ParsedDocument(
            filename=self.filename,
            file_type="xlsx",
            content=sheets_data,
            metadata=self._get_metadata(),
            sections=sheets_data
        )


class MarkdownParser(DocumentParser):
    """Markdown 文档解析器 (.md)"""
    
    def parse(self) -> ParsedDocument:
        import markdown
        from bs4 import BeautifulSoup
        
        # 读取 Markdown 内容
        with open(self.file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 转换为 HTML
        html_content = markdown.markdown(md_content)
        
        # 解析 HTML 提取结构
        soup = BeautifulSoup(html_content, 'html.parser')
        
        sections = []
        current_section = {"title": None, "content": []}
        
        for elem in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'table']):
            if elem.name.startswith('h'):
                # 如果是标题，保存之前的 section
                if current_section["content"]:
                    sections.append(current_section)
                current_section = {
                    "title": elem.get_text().strip(),
                    "level": int(elem.name[1]),
                    "content": []
                }
            elif elem.name == 'p':
                text = elem.get_text().strip()
                if text:
                    current_section["content"].append({"type": "paragraph", "text": text})
            elif elem.name in ['ul', 'ol']:
                items = [li.get_text().strip() for li in elem.find_all('li')]
                current_section["content"].append({"type": "list", "items": items})
            elif elem.name == 'table':
                table_data = []
                for row in elem.find_all('tr'):
                    row_data = [cell.get_text().strip() for cell in row.find_all(['td', 'th'])]
                    table_data.append(row_data)
                current_section["content"].append({"type": "table", "data": table_data})
        
        # 添加最后一个 section
        if current_section["content"]:
            sections.append(current_section)
        
        return ParsedDocument(
            filename=self.filename,
            file_type="md",
            content=md_content,
            metadata=self._get_metadata(),
            sections=sections
        )


class TxtParser(DocumentParser):
    """TXT 文本解析器 (.txt)"""
    
    def parse(self) -> ParsedDocument:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按段落分割
        paragraphs = []
        for para in content.split('\n\n'):
            para = para.strip()
            if para:
                paragraphs.append({
                    "type": "paragraph",
                    "text": para
                })
        
        return ParsedDocument(
            filename=self.filename,
            file_type="txt",
            content=content,
            metadata=self._get_metadata(),
            sections=paragraphs
        )


class ParserFactory:
    """解析器工厂类"""
    
    _parsers = {
        '.docx': WordParser,
        '.xlsx': ExcelParser,
        '.md': MarkdownParser,
        '.txt': TxtParser,
    }
    
    @classmethod
    def get_parser(cls, file_path: str) -> DocumentParser:
        """根据文件类型获取对应的解析器"""
        ext = Path(file_path).suffix.lower()
        
        if ext not in cls._parsers:
            raise ValueError(f"不支持的文件类型: {ext}，支持的类型: {list(cls._parsers.keys())}")
        
        return cls._parsers[ext](file_path)
    
    @classmethod
    def parse_file(cls, file_path: str) -> ParsedDocument:
        """解析文件并返回结果"""
        parser = cls.get_parser(file_path)
        return parser.parse()
    
    @classmethod
    def register_parser(cls, extension: str, parser_class: type):
        """注册新的解析器"""
        cls._parsers[extension.lower()] = parser_class


def parse_document(file_path: str) -> ParsedDocument:
    """
    解析文档的便捷函数
    
    Args:
        file_path: 文件路径
        
    Returns:
        ParsedDocument: 解析后的文档对象
    """
    return ParserFactory.parse_file(file_path)


if __name__ == "__main__":
    # 测试代码
    import sys
    
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        try:
            result = parse_document(test_file)
            print(result.to_json())
        except Exception as e:
            print(f"解析失败: {e}")
    else:
        print("用法: python parser.py <文件路径>")
