# 项目概览与快速参考

## 1. 项目结构

```
D2E/
├── backend/                # 后端代码
│   ├── app/                # 应用核心代码
│   │   ├── services/       # 核心服务模块
│   │   │   ├── parser.py   # 文档解析模块（已完成）
│   │   │   ├── extractor.py # 信息抽取模块（已完成）
│   │   │   ├── matcher.py  # 字段语义匹配模块（已完成）
│   │   │   ├── filler.py   # 自动填表模块（已完成）
│   │   │   └── knowledge_pool.py # 知识池模块（已完成）
│   │   ├── utils/          # 工具模块
│   │   │   ├── helpers.py  # 辅助函数
│   │   │   ├── regex_patterns.py # 正则表达式模式
│   │   │   └── vectorizer.py # 向量化工具
│   │   ├── main.py         # API入口（已完成）
│   │   ├── models.py       # 数据模型
│   │   ├── database.py     # 数据库连接
│   │   └── config.py       # 配置文件
│   ├── data/               # 数据目录
│   │   ├── test_set/       # 测试数据集
│   │   └── test_output/    # 测试输出
│   ├── tests/              # 测试脚本
│   ├── requirements.txt    # 依赖文件
│   └── start.py            # 启动脚本
├── docs/                   # 文档
│   ├── AIReadMe.md        # AI参考文档
│   └── ProjectOverview.md # 项目概览（本文件）
├── frontend/               # 前端代码
├── scripts/                # 脚本文件
├── tests/                  # 测试报告
└── README.md               # 项目说明
```

## 2. 核心模块功能

### 2.1 文档解析模块 (parser.py)
- **功能**：支持 Word、Excel、Markdown、TXT 格式文档解析
- **输出**：统一 JSON 结构，包含 doc_id、paragraphs、tables、raw_text
- **特殊处理**：Word 文件添加了备用解析方案（使用 zipfile + XML 解析）

### 2.2 信息抽取模块 (extractor.py)
- **功能**：从文档中抽取实体（金额、日期、百分比、电话、邮箱等）
- **方法**：正则表达式、NER 模型（可选）、大语言模型（可选）
- **输出**：实体列表，包含实体类型、值、来源文档、段落索引、置信度

### 2.3 语义匹配模块 (matcher.py)
- **功能**：将模板字段与抽取实体进行语义对齐
- **技术**：使用 sentence-transformers 计算语义相似度
- **回退方案**：当模型加载失败时，使用简单的字符串匹配

### 2.4 自动填表模块 (filler.py)
- **功能**：根据模板生成 Excel 或 Word 结果文件
- **支持格式**：.xlsx、.docx
- **填充方式**：Excel 按列填充，Word 替换 {字段} 占位符

### 2.5 知识池模块 (knowledge_pool.py)
- **功能**：存储文档和实体信息，支持快速查询
- **技术**：SQLite 数据库
- **主要方法**：保存文档、获取实体、删除文档

## 3. API 接口

| 接口 | 方法 | 功能 | 参数 | 返回值 |
|------|------|------|------|--------|
| `/upload_docs` | POST | 上传文档并解析抽取实体 | 多文件（.docx, .xlsx, .md, .txt） | `{"doc_ids": [...], "message": "success"}` |
| `/fill_template` | POST | 上传模板并自动填表 | 模板文件（.xlsx, .docx） | 填充后的文件（二进制下载） |
| `/entities` | GET | 查询指定文档的实体 | doc_id（文档ID） | 实体列表 |
| `/` | GET | 根路径 | 无 | 系统欢迎信息 |

## 4. 技术栈

| 类别 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.115.11 |
| ASGI 服务器 | uvicorn | 0.34.0 |
| 文档解析 | python-docx | 1.1.2 |
| 表格处理 | pandas | 2.2.3 |
| Excel 操作 | openpyxl | 3.1.5 |
| Markdown 解析 | markdown | 3.7 |
| 语义向量 | sentence-transformers | 3.3.1 |
| 深度学习框架 | torch | 2.6.0 |
| 代码格式化 | black | 25.1.0 |
| 单元测试 | pytest | 8.3.4 |

## 5. 数据格式

### 5.1 文档解析输出
```json
{
  "doc_id": "string",
  "paragraphs": ["string"],
  "tables": [[["string"]]],
  "raw_text": "string"
}
```

### 5.2 实体记录格式
```json
{
  "entity_type": "string",
  "value": "string",
  "source_doc": "string",
  "paragraph_index": "int",
  "confidence": "float"
}
```

## 6. 测试状态

- **文档解析模块**：已完成测试，支持所有格式
- **信息抽取模块**：已完成测试，从 4 个文档中抽取 4,756 个实体
- **语义匹配模块**：已实现，包含回退方案
- **自动填表模块**：已实现，支持 Excel 和 Word 模板
- **知识池模块**：已实现，使用 SQLite 存储
- **API 接口**：已实现所有接口

## 7. 快速启动

1. **安装依赖**：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **启动服务**：
   ```bash
   python app/main.py
   ```

3. **访问 API**：
   - 服务地址：http://localhost:8000
   - API 文档：http://localhost:8000/docs

## 8. 核心工作流程

1. **文档上传**：用户上传多种格式的文档
2. **文档解析**：将文档转换为统一 JSON 结构
3. **信息抽取**：从文档中抽取实体
4. **知识存储**：将文档和实体存入知识池
5. **模板上传**：用户上传 Excel 或 Word 模板
6. **字段提取**：从模板中提取字段
7. **语义匹配**：将模板字段与知识池中的实体进行匹配
8. **自动填表**：根据匹配结果填充模板
9. **结果返回**：返回填充后的文件

## 9. 性能优化

- **缓存机制**：解析结果缓存到数据库，避免重复计算
- **并行处理**：支持多线程处理文档
- **模型优化**：使用轻量级语义向量模型
- **错误处理**：所有外部调用都有 try-catch 保护

## 10. 扩展建议

1. **增加 PDF 支持**：添加 PDF 文档解析功能
2. **增强 LLM 集成**：接入更多大语言模型 API
3. **优化前端**：使用 Streamlit 或 Gradio 构建更丰富的前端界面
4. **添加批量处理**：支持批量文档处理和批量填表
5. **数据可视化**：添加数据可视化功能，直观展示抽取和匹配结果