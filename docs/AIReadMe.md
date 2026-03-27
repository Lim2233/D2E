以下是一份 **AI 参考文档**，旨在为后续的代码生成、模块设计、问题解答等任务提供统一的项目上下文。AI 将以此文档为依据进行工作，确保输出内容与项目目标、技术规范和团队约定保持一致。

---

# 项目技术规范与 AI 参考文档

## 1. 项目概述

本项目为“基于大语言模型的文档理解与多源数据融合系统”，目标是构建一个能够自动解析多种格式文档（Word、Excel、Markdown、TXT）、抽取关键信息、语义匹配字段并自动填表的智能系统。系统需满足竞赛评测的高准确率与低响应时间要求。

### 核心能力
- 多格式文档统一解析
- 信息抽取（规则 + 模型 + 大语言模型）
- 字段语义匹配（向量相似度 + 规则校验）
- 知识池存储（一次解析，多次查询）
- 自动填表（Excel/Word 模板）

---

## 2. 系统架构与模块划分

系统采用模块化设计，各模块职责明确，通过统一数据接口通信。

| 模块 | 职责 | 关键技术 |
|------|------|----------|
| 文档解析模块 | 读取 .docx/.xlsx/.md/.txt，转换为统一 JSON 结构 | python-docx, pandas, openpyxl |
| 信息抽取模块 | 从文本中识别实体（金额、日期、项目名称等） | 正则表达式 + NER 模型 + 大语言模型 |
| 字段语义匹配模块 | 将模板字段与抽取实体进行语义对齐 | sentence-transformers, 向量相似度 |
| 知识池模块 | 存储实体信息，支持快速查询 | SQLite / MongoDB |
| 自动填表模块 | 根据模板生成 Excel 或 Word 结果文件 | openpyxl, python-docx |
| 系统整合与性能优化 | 提供 API 接口、缓存、并发、日志管理 | FastAPI, ThreadPoolExecutor |
| 前端与展示 | 文件上传界面、结果可视化、答辩材料 | Streamlit / Gradio |

---

## 3. 数据格式定义

所有模块间通信必须遵循以下 JSON 格式。

### 3.1 文档解析输出

```json
{
  "doc_id": "string",
  "paragraphs": ["string"],
  "tables": [[["string"]]],
  "raw_text": "string"
}
```

- `paragraphs`：文本段落列表
- `tables`：三维列表，第一维为表格序号，第二维为行，第三维为单元格内容
- `raw_text`：全文拼接文本（用于后续语义分析）

### 3.2 实体记录格式

```json
{
  "entity_type": "string",
  "value": "string",
  "source_doc": "string",
  "paragraph_index": "int",
  "confidence": "float"
}
```

- `entity_type`：实体类型，如“合同金额”“项目名称”
- `value`：归一化后的值（如金额转换为数字字符串）
- `source_doc`：来源文档 ID 或文件名
- `paragraph_index`：所在段落索引（从 0 开始）
- `confidence`：置信度，范围 0–1

### 3.3 知识池存储结构

数据库表或集合包含：
- `doc_id`
- `parsed_content`（JSON 格式）
- `entities`（实体列表）
- `create_time`

---

## 4. 技术栈与依赖

| 类别 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 文档解析 | python-docx, pandas, openpyxl, markdown |
| 信息抽取 | re (正则), HuggingFace Transformers (可选), OpenAI API (可选) |
| 语义匹配 | sentence-transformers |
| 数据库 | SQLite 或 MongoDB |
| 前端 | Streamlit 或 Gradio |
| 并发 | ThreadPoolExecutor |
| 缓存 | 内存缓存或 Redis |

**Python 版本**：3.10+

---

## 5. API 接口约定（后端）

系统需提供以下 REST API 供前端调用：

### 5.1 上传文档
- `POST /upload_docs`
- 输入：多文件（支持 .docx, .xlsx, .md, .txt）
- 输出：`{ "doc_ids": ["doc1", "doc2"], "message": "success" }`
- 行为：解析文档，抽取实体，存入知识池

### 5.2 上传模板并填表
- `POST /fill_template`
- 输入：模板文件（.xlsx 或 .docx）
- 输出：生成的结果文件（二进制下载）
- 行为：读取模板字段，语义匹配实体，生成填表结果

### 5.3 查询知识池（调试用）
- `GET /entities?doc_id=xxx`
- 输出：该文档的所有实体列表

---

## 6. 开发规范

### 6.1 目录结构

```
project/
├── backend/
│   ├── app/                 # 应用核心代码
│   │   ├── services/        # 核心业务逻辑
│   │   │   ├── parser.py        # 文档解析（已完成）
│   │   │   ├── extractor.py     # 信息抽取（已完成）
│   │   │   ├── matcher.py       # 语义匹配
│   │   │   ├── filler.py        # 自动填表
│   │   │   └── knowledge_pool.py # 知识池
│   │   ├── main.py              # 应用入口
│   │   └── models.py           # 数据模型
│   ├── data/                # 数据目录
│   │   ├── test_set/       # 测试数据集
│   │   └── test_output/    # 测试输出（gitignore）
│   ├── test_parser.py       # 文档解析测试脚本
│   ├── test_extractor.py    # 信息抽取测试脚本
│   └── requirements.txt
├── docs/                   # 文档
├── frontend/               # 前端代码
└── README.md
```

### 6.2 代码风格
- 使用 `black` 自动格式化
- 函数、类、模块必须有 docstring
- 类型注解必须完整

### 6.3 错误处理
- 所有外部调用（文件读取、模型推理）必须 `try-catch`
- 错误信息通过 API 返回 `{ "error": "description" }`，状态码 400/500

---

## 7. 性能与测试要求

### 7.1 性能指标
- 单文档解析 + 抽取 ≤ 5 秒
- 10 个文档批量处理总时间 ≤ 30 秒
- 填表响应时间 ≤ 3 秒

### 7.2 优化策略
- 解析结果缓存到数据库，避免重复计算
- 实体向量提前计算并存储
- 多线程并行处理文档

### 7.3 测试要求
- 提供至少 5 个不同格式的测试文档
- 提供至少 3 个模板表格（包含不同字段组合）
- 单元测试覆盖核心模块（解析、抽取、匹配）

---

## 8. 团队分工与协作（供 AI 参考）

虽然 AI 不直接参与团队协作，但了解分工有助于生成针对性代码或建议。

| 模块 | 负责人 | AI 可协助方向 |
|------|--------|----------------|
| 文档解析模块 | P1 | 生成解析代码模板，处理不同格式 |
| 信息抽取模块 | P2 | 提供正则表达式示例、NER 模型调用代码 |
| 语义匹配模块 | P3 | 实现向量化与相似度计算 |
| 系统整合与性能优化 | P4 | 设计 API 结构、缓存机制、多线程示例 |
| 前端与展示 | P5 | 生成前端界面代码、可视化组件 |

---

## 9. 常见任务示例（AI 工作指引）

当 AI 被要求完成具体任务时，应参考本规范生成符合项目上下文的内容。以下列举常见任务类型：

### 9.1 生成模块代码
- 要求：实现文档解析模块，支持 .docx 和 .txt
- 输出：符合第 3 节 JSON 格式的 Python 函数
- 状态：已完成（支持 Word、Excel、Markdown、TXT）

### 9.2 设计数据库模型
- 要求：设计知识池的 SQLite 表结构
- 输出：包含 `documents` 和 `entities` 表的 SQL DDL
- 状态：待实现

### 9.3 编写 API 路由
- 要求：实现 `/fill_template` 接口
- 输出：FastAPI 路由代码，包含请求验证、调用核心模块、返回文件
- 状态：待实现

### 9.4 优化性能
- 要求：为文档解析模块添加多线程支持
- 输出：使用 `ThreadPoolExecutor` 的代码示例
- 状态：待实现

## 10. 已完成模块说明

### 10.1 文档解析模块（parser.py）
- 支持格式：Word (.docx)、Excel (.xlsx)、Markdown (.md)、TXT (.txt)
- 输出格式：统一的 JSON 结构，包含 doc_id、paragraphs、tables、raw_text
- 特殊处理：Word 文件添加了备用解析方案（使用 zipfile + XML 解析）
- 测试状态：已通过测试，所有格式解析正常

### 10.2 信息抽取模块（extractor.py）
- 支持方法：正则表达式、NER 模型（可选）、大语言模型（可选）
- 抽取实体类型：金额、日期、百分比、电话、邮箱等
- 测试状态：已通过测试，从 4 个文档中抽取 4,756 个实体
- 测试脚本：test_extractor.py

## 11. 待完成模块

### 11.1 字段语义匹配模块（matcher.py）
- 功能：将模板字段与抽取实体进行语义对齐
- 技术：sentence-transformers、向量相似度计算
- 状态：待实现

### 11.2 知识池模块（knowledge_pool.py）
- 功能：存储实体信息，支持快速查询
- 技术：SQLite / MongoDB
- 状态：待实现

### 11.3 自动填表模块（filler.py）
- 功能：根据模板生成 Excel 或 Word 结果文件
- 技术：openpyxl、python-docx
- 状态：待实现

### 11.4 API 接口（main.py）
- 功能：提供 REST API 供前端调用
- 接口：/upload_docs、/fill_template、/entities
- 状态：待实现

---

## 10. 项目约束与假设

- 所有文档均为中文或英文
- 模板表格第一行为字段名称
- 系统不依赖外部云服务（大语言模型可选，但需有本地回退方案）
- 竞赛环境为本地运行，无需部署到云端

---

本文档将作为 AI 执行任务时的唯一上下文依据，所有生成内容必须符合上述规范。若需修改或扩展规范，请先提出变更说明。