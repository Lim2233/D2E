#!/usr/bin/env python3
"""
简单的 HTTP 服务器，不依赖 asyncio
"""
import http.server
import socketserver
import json
import os
import tempfile
from urllib.parse import parse_qs

# 初始化知识池（简化版）
class KnowledgePool:
    def __init__(self):
        self.documents = {}
    
    def save_document(self, doc_id, parsed_doc, entities):
        self.documents[doc_id] = {"parsed_doc": parsed_doc, "entities": entities}
    
    def get_entities_by_doc_id(self, doc_id):
        return self.documents.get(doc_id, {}).get("entities", [])
    
    def get_all_entities(self):
        all_entities = []
        for doc in self.documents.values():
            all_entities.extend(doc.get("entities", []))
        return all_entities

knowledge_pool = KnowledgePool()

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "文档理解与多源数据融合系统 API"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path.startswith('/entities'):
            # 解析查询参数
            query_string = self.path.split('?', 1)[1] if '?' in self.path else ''
            params = parse_qs(query_string)
            doc_id = params.get('doc_id', [None])[0]
            
            if not doc_id:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "doc_id is required"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            entities = knowledge_pool.get_entities_by_doc_id(doc_id)
            if not entities:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": f"文档 {doc_id} 不存在或无实体"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(entities).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_POST(self):
        if self.path == '/upload_docs':
            # 简化处理，实际项目中需要解析文件上传
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"doc_ids": ["test123"], "message": "success"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == '/fill_template':
            # 简化处理，实际项目中需要解析文件上传
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "Template filled successfully"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

def run_server():
    PORT = 8000
    Handler = SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"服务器运行在 http://localhost:{PORT}")
        print(f"根路径: http://localhost:{PORT}/")
        print(f"实体查询: http://localhost:{PORT}/entities?doc_id=xxx")
        print(f"上传文档: POST http://localhost:{PORT}/upload_docs")
        print(f"填充模板: POST http://localhost:{PORT}/fill_template")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
