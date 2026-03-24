import os

# 项目根目录（当前目录）
ROOT = os.getcwd()

# 需要创建的目录结构（相对于根目录）
directories = [
    "backend/app",
    "backend/app/services",
    "backend/app/utils",
    "backend/tests",
    "backend/data/uploads",
    "backend/data/templates",
    "backend/data/output",
    "frontend",
    "scripts",
    "docs"
]

# 需要创建的空文件（相对于根目录）
files = [
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/config.py",
    "backend/app/models.py",
    "backend/app/database.py",
    "backend/app/services/__init__.py",
    "backend/app/services/parser.py",
    "backend/app/services/extractor.py",
    "backend/app/services/matcher.py",
    "backend/app/services/filler.py",
    "backend/app/services/knowledge_pool.py",
    "backend/app/utils/__init__.py",
    "backend/app/utils/regex_patterns.py",
    "backend/app/utils/vectorizer.py",
    "backend/app/utils/helpers.py",
    "backend/tests/__init__.py",
    "backend/tests/test_parser.py",
    "frontend/index.html",
    "scripts/init_db.py",
    "scripts/test_sample.py",
    "README.md",
    ".gitignore"
]

# 创建目录
for d in directories:
    path = os.path.join(ROOT, d)
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {path}")

# 创建空文件
for f in files:
    path = os.path.join(ROOT, f)
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as fp:
            pass
        print(f"Created file: {path}")
    else:
        print(f"File already exists: {path}")

# 创建 requirements.txt 并写入基础依赖
req_path = os.path.join(ROOT, "backend", "requirements.txt")
if not os.path.exists(req_path):
    with open(req_path, 'w', encoding='utf-8') as fp:
        fp.write("""fastapi==0.104.1
uvicorn[standard]==0.24.0
python-docx==1.1.0
openpyxl==3.1.2
markdown==3.5.1
pandas==2.1.3
sentence-transformers==2.2.2
LAC==2.1.2
openai==1.3.0
python-multipart
pydantic[dotenv]==2.5.0
""")
    print(f"Created file: {req_path}")
else:
    print(f"File already exists: {req_path}")

# 创建 .gitignore 内容
gitignore_path = os.path.join(ROOT, ".gitignore")
if not os.path.exists(gitignore_path):
    with open(gitignore_path, 'w', encoding='utf-8') as fp:
        fp.write("""# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/

# Data
backend/data/uploads/
backend/data/templates/
backend/data/output/
*.db
*.sqlite

# Logs
*.log

# OS
.DS_Store
Thumbs.db
""")
    print(f"Created file: {gitignore_path}")
else:
    print(f"File already exists: {gitignore_path}")

print("\nProject structure created successfully!")