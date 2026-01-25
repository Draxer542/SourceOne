<div align="center">
  <img src="app/static/SourceOneLogo.png" alt="SourceOne Logo" width="200" height="200">
  <h1>SourceOne</h1>
  <p>A comprehensive Retrieval-Augmented Generation (RAG) system for intelligent document processing and context-aware responses</p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square&logo=python)](https://www.python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## 🎯 Overview

**SourceOne** is a cutting-edge Retrieval-Augmented Generation (RAG) system that combines the power of document processing, intelligent semantic search, and large language models. Whether you're building a smart Q&A system, an intelligent document assistant, or a context-aware chatbot, SourceOne provides a robust foundation for these applications.

With SourceOne, you can:
- 📄 Upload and process multiple document formats
- 🔍 Perform hybrid search with ranking and reranking
- 🤖 Generate intelligent, context-aware responses
- ⚡ Leverage state-of-the-art LLMs (OpenAI)
- 🎯 Build production-ready RAG applications

---

## ✨ Features

### Document Management
- **Multi-format Support**: Upload and process various document types
- **Intelligent Chunking**: Automatic document segmentation for optimal retrieval
- **Metadata Extraction**: Preserve and utilize document metadata

### Advanced Search Capabilities
- **Hybrid Search**: Combine semantic and keyword-based search
- **Reranking**: Intelligent result ranking using cross-encoders
- **Vector Storage**: Efficient storage using ChromaDB
- **Semantic Understanding**: Leverage embeddings for context-aware retrieval

### Response Generation
- **Context-Aware Responses**: Generate answers grounded in retrieved documents
- **OpenAI Integration**: Utilize powerful language models
- **Streaming Support**: Real-time response generation
- **Citation Tracking**: Know where your answers come from

### Production-Ready
- **REST API**: Easy-to-use FastAPI endpoints
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed logging for debugging and monitoring
- **Scalable Architecture**: Built for growth

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend Framework** | FastAPI | High-performance REST API |
| **LLM Framework** | LangChain | Orchestrating LLM workflows |
| **Vector Database** | ChromaDB | Efficient document embeddings storage |
| **Language Model** | OpenAI API | State-of-the-art text generation |
| **Frontend** | HTML5 | User interface |

**Language Composition:**
- Python: 39.2% (Backend Logic)
- HTML: 60.8% (Frontend)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         User Interface (HTML/Frontend)       │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│          FastAPI REST API Server             │
│  ├─ /upload (Document Upload)               │
│  ├─ /search (Retrieve Documents)            │
│  ├─ /query (Generate Response)              │
│  └─ /health (System Status)                 │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼────────┐
│  LangChain     │   │  ChromaDB       │
│  (Orchestration)   │  (Vector Store) │
└───────┬────────┘   └────────┬────────┘
        │                     │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   OpenAI API        │
        │  (Language Models)  │
        └─────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:
- **Python 3.8+** installed
- **pip** package manager
- **OpenAI API Key** (get one at [platform.openai.com](https://platform.openai.com))
- **Git** for version control

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Draxer542/SourceOne.git
   cd SourceOne
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Environment Variables**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4
   CHROMA_DB_PATH=./chroma_db
   LOG_LEVEL=INFO
   ```

2. **Update Configuration** (if needed)
   
   Modify `config.py` to customize:
   - Chunk size and overlap for document processing
   - Model parameters and temperature
   - Vector database settings

---

## 💡 Usage

### Starting the Server

```bash
# Development mode
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

Access the API at `http://localhost:8000`

### Interactive API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Example: Upload and Query

```python
import requests

# Upload a document
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/upload",
        files={"file": f}
    )
    print(response.json())

# Query the system
response = requests.post(
    "http://localhost:8000/query",
    json={"query": "What is the main topic of the document?"}
)
print(response.json())
```

---

## 📡 API Endpoints

### Document Management

#### Upload Document
```
POST /upload
Content-Type: multipart/form-data

Parameters:
- file: Document file (PDF, TXT, DOCX, etc.)

Response:
{
  "file_id": "doc_123",
  "filename": "document.pdf",
  "chunks_created": 15,
  "status": "success"
}
```

#### List Documents
```
GET /documents

Response:
{
  "documents": [
    {
      "file_id": "doc_123",
      "filename": "document.pdf",
      "upload_date": "2026-01-25T10:30:00Z",
      "chunk_count": 15
    }
  ]
}
```

### Search and Query

#### Search Documents
```
POST /search
Content-Type: application/json

Request:
{
  "query": "search term",
  "top_k": 5
}

Response:
{
  "results": [
    {
      "score": 0.95,
      "content": "...",
      "source": "document.pdf",
      "metadata": {}
    }
  ]
}
```

#### Generate Response
```
POST /query
Content-Type: application/json

Request:
{
  "query": "Your question here",
  "context_window": 5,
  "temperature": 0.7
}

Response:
{
  "answer": "Generated response...",
  "sources": ["document.pdf"],
  "confidence": 0.92,
  "processing_time_ms": 1250
}
```

### System Health

#### Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "llm": "connected"
}
```

---

## 📁 Project Structure

```
SourceOne/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── models/
│   │   ├── request.py          # Request models
│   │   └── response.py         # Response models
│   ├── routes/
│   │   ├── documents.py        # Document endpoints
│   │   ├── search.py           # Search endpoints
│   │   └── health.py           # Health check endpoints
│   ├── services/
│   │   ├── document_processor.py  # Document handling
│   │   ├── retriever.py           # Retrieval logic
│   │   └── llm_handler.py         # LLM interactions
│   └── utils/
│       ├── logger.py           # Logging configuration
│       └── helpers.py          # Utility functions
├── frontend/
│   ├── index.html              # Web interface
│   ├── styles.css              # Styling
│   └── script.js               # Frontend logic
├── tests/
│   ├── test_documents.py       # Document tests
│   ├── test_search.py          # Search tests
│   └── test_api.py             # API tests
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker configuration
├── Dockerfile                  # Container definition
├── README.md                   # This file
└── LICENSE                     # MIT License
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the Repository**
   ```bash
   gh repo fork Draxer542/SourceOne
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Your Changes**
   - Follow PEP 8 style guidelines
   - Add tests for new functionality
   - Update documentation as needed

4. **Commit Your Changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push to Your Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Provide a clear description of your changes
   - Reference any related issues

---

### Community
- 🐛 [Issue Tracker](https://github.com/Draxer542/SourceOne/issues)

---

### Contact
- 📧 Email: draxertechupdates@gmail.com

---

<div align="center">
  <p><a href="https://github.com/Draxer542/SourceOne">⭐ Give us a star on GitHub!</a></p>
</div>
