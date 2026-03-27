"""
Flask 应用入口，作为 FastAPI 的替代方案
"""
import os
import tempfile
from flask import Flask, request, jsonify, send_file
from typing import List

from app.services.parser import parse_document
from app.services.extractor import extract_entities
from app.services.matcher import match_entities
from app.services.filler import fill_template, extract_template_fields
from app.services.knowledge_pool import KnowledgePool

# 创建 Flask 应用
app = Flask(__name__)

# 初始化知识池
knowledge_pool = KnowledgePool()


@app.route('/upload_docs', methods=['POST'])
def upload_docs():
    """
    上传文档并解析抽取实体
    """
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400
    
    files = request.files.getlist('files')
    doc_ids = []
    
    for file in files:
        # 检查文件类型
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.docx', '.xlsx', '.md', '.txt']:
            return jsonify({"error": f"不支持的文件格式: {file_ext}"}), 400
        
        # 保存临时文件
        with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as tmp:
            content = file.read()
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
    
    return jsonify({"doc_ids": doc_ids, "message": "success"})


@app.route('/fill_template', methods=['POST'])
def fill_template_endpoint():
    """
    上传模板并自动填表
    """
    if 'template' not in request.files:
        return jsonify({"error": "No template provided"}), 400
    
    template = request.files['template']
    # 检查文件类型
    file_ext = os.path.splitext(template.filename)[1].lower()
    if file_ext not in ['.xlsx', '.docx']:
        return jsonify({"error": f"不支持的模板格式: {file_ext}"}), 400
    
    # 保存临时文件
    with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as tmp:
        content = template.read()
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
        return send_file(
            path_or_file=output_path,
            filename=f"filled_{template.filename}",
            as_attachment=True
        )
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route('/entities', methods=['GET'])
def get_entities():
    """
    查询指定文档的实体
    """
    doc_id = request.args.get('doc_id')
    if not doc_id:
        return jsonify({"error": "doc_id is required"}), 400
    
    entities = knowledge_pool.get_entities_by_doc_id(doc_id)
    if not entities:
        return jsonify({"error": f"文档 {doc_id} 不存在或无实体"}), 404
    return jsonify(entities)


@app.route('/')
def root():
    """
    根路径
    """
    return jsonify({"message": "文档理解与多源数据融合系统 API"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
