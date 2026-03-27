"""
FastAPI 应用入口，定义所有 API 路由和启动逻辑
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import tempfile
from typing import List

from app.services.parser import parse_document
from app.services.extractor import extract_entities
from app.services.matcher import match_entities
from app.services.filler import fill_template, extract_template_fields
from app.services.knowledge_pool import KnowledgePool
from app.database import get_db_connection

# 创建 FastAPI 应用
app = FastAPI(
    title="文档理解与多源数据融合系统",
    description="基于大语言模型的文档解析、信息抽取与自动填表系统",
    version="1.0.0"
)

# 初始化知识池
knowledge_pool = KnowledgePool()


@app.post("/upload_docs")
async def upload_docs(files: List[UploadFile] = File(...)):
    """
    上传文档并解析抽取实体
    """
    doc_ids = []
    
    for file in files:
        # 检查文件类型
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.docx', '.xlsx', '.md', '.txt']:
            raise HTTPException(status_code=400, detail=f"不支持的文件格式: {file_ext}")
        
        # 保存临时文件
        with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            temp_path = tmp.name
        
        try:
            # 解析文档
            parsed_doc = parse_document(temp_path)
            doc_id = parsed_doc['doc_id']
            doc_ids.append(doc_id)
            
            # 抽取实体
            entities = extract_entities(parsed_doc)
            
            # 存入知识池
            knowledge_pool.save_document(doc_id, parsed_doc, entities)
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    return {"doc_ids": doc_ids, "message": "success"}


@app.post("/fill_template")
async def fill_template_endpoint(template: UploadFile = File(...)):
    """
    上传模板并自动填表
    """
    # 检查文件类型
    file_ext = os.path.splitext(template.filename)[1].lower()
    if file_ext not in ['.xlsx', '.docx']:
        raise HTTPException(status_code=400, detail=f"不支持的模板格式: {file_ext}")
    
    # 保存临时文件
    with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as tmp:
        content = await template.read()
        tmp.write(content)
        temp_path = tmp.name
    
    try:
        # 提取模板字段
        template_fields = extract_template_fields(temp_path)
        
        # 从知识池获取所有实体
        all_entities = knowledge_pool.get_all_entities()
        
        # 语义匹配
        matches = match_entities(template_fields, all_entities)
        
        # 填充模板
        output_path = fill_template(temp_path, matches)
        
        # 返回生成的文件
        return FileResponse(
            path=output_path,
            filename=f"filled_{template.filename}",
            media_type="application/octet-stream"
        )
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.get("/entities")
async def get_entities(doc_id: str):
    """
    查询指定文档的实体
    """
    entities = knowledge_pool.get_entities_by_doc_id(doc_id)
    if not entities:
        raise HTTPException(status_code=404, detail=f"文档 {doc_id} 不存在或无实体")
    return entities


@app.get("/")
async def root():
    """
    根路径
    """
    return {"message": "文档理解与多源数据融合系统 API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)