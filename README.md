<div align="center">
  <img src="app/static/SourceOneLogo.png" alt="SourceOne Logo" width="200" height="200">
  
  # SourceOne
  
  ### Enterprise-Grade RAG System with Authentication & Conversation History
  
  **Intelligent Document Processing | Context-Aware AI Responses | Secure Multi-User Platform**
  
  [![Python](https://img.shields.io/badge/Python-3.13+-3776ab?style=flat-square&logo=python)](https://www.python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
  [![LangChain](https://img.shields.io/badge/🦜_LangChain-0.1+-blue?style=flat-square)](https://www.langchain.com)
  [![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
  
  [Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-api-documentation) • [Architecture](#-architecture) • [Contributing](#-contributing)
  
</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Advanced Features](#-advanced-features)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)
- [Support](#-support)

---

## 🎯 Overview

**SourceOne** is a production-ready Retrieval-Augmented Generation (RAG) system that combines cutting-edge AI technology with enterprise features. Built with FastAPI, LangChain, and ChromaDB, it provides secure document processing, intelligent search, and context-aware responses powered by large language models.

### Why SourceOne?

- **🔐 Enterprise Security**: JWT-based authentication, user isolation, and secure sessions
- **💬 Conversation Memory**: Persistent chat history with contextual query understanding
- **🔍 Hybrid Search**: Combines BM25 keyword search with semantic vector similarity
- **⚡ Real-Time Streaming**: Server-Sent Events (SSE) for instant AI responses
- **📊 Smart Reranking**: FlashRank-powered relevance optimization
- **🎨 Modern UI**: Clean, responsive interface with markdown rendering and LaTeX support

---

## ✨ Key Features

### 🔐 Authentication & Security
- **JWT Token Authentication**: Secure, stateless authentication
- **User Registration & Login**: Email-based user accounts with password hashing (bcrypt)
- **Session Management**: Automatic token expiration and renewal
- **User Isolation**: Each user's documents and conversations are private

### 💬 Conversation Management
- **Persistent Chat History**: Store and retrieve conversation threads
- **Context-Aware Queries**: Automatic query contextualization using chat history
- **Conversation Threads**: Organize interactions into manageable sessions
- **History Sidebar**: Quick access to recent conversations

### 📄 Document Processing
- **Multi-Format Support**: PDF, Markdown, TXT, DOCX (up to 3 files simultaneously)
- **Intelligent Chunking**: RecursiveCharacterTextSplitter with 1000-char chunks, 200-char overlap
- **Metadata Preservation**: Source tracking, page numbers, and custom attributes
- **Background Processing**: Non-blocking uploads with async indexing

### 🔍 Advanced Retrieval
- **Hybrid Search Engine**: 
  - BM25 keyword-based retrieval (statistical)
  - Vector similarity search (semantic embeddings)
  - Ensemble merging with 50/50 weighting
- **Smart Reranking**: FlashRank cross-encoder (ms-marco-MiniLM-L-12-v2)
- **Top-K Retrieval**: Configurable result limits (default: 10 → 5 after reranking)
- **Lazy Initialization**: Models load on-demand for faster startup

### 🤖 AI-Powered Generation
- **LLM Integration**: NVIDIA GPT-OSS-20B via OpenAI-compatible API
- **Streaming Responses**: Real-time token generation with SSE
- **Contextual Answers**: Grounded responses from retrieved documents
- **Citation Tracking**: Source documents displayed with each answer
- **History-Aware Prompting**: Reformulates queries based on conversation context

### 🎨 Modern User Interface
- **Responsive Design**: Mobile-first, works on all devices
- **Markdown Rendering**: Full support with marked.js and DOMPurify
- **LaTeX Math**: KaTeX rendering for mathematical expressions
- **Syntax Highlighting**: Code blocks with highlight.js and copy-to-clipboard
- **Collapsible Sidebar**: Chat history navigation with recent conversations
- **Dark Mode Ready**: Design tokens for easy theming

---

## 🛠️ Tech Stack

### Backend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **API Framework** | FastAPI 0.100+ | Async REST API with automatic OpenAPI docs |
| **Authentication** | JWT (python-jose) | Secure token-based auth |
| **Password Hashing** | bcrypt | Industry-standard password security |
| **Database** | SQLAlchemy + SQLite | User accounts & conversation history |
| **Embeddings** | HuggingFace Transformers | sentence-transformers/all-MiniLM-L6-v2 |
| **Vector Store** | ChromaDB | Persistent vector embeddings storage |
| **Search** | BM25 + Vector Hybrid | Keyword + semantic search |
| **Reranking** | FlashRank | Cross-encoder relevance scoring |
| **LLM** | NVIDIA GPT-OSS-20B | Natural language generation |
| **Orchestration** | LangChain | LLM workflow management |

### Frontend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **UI** | Vanilla JavaScript | No framework dependencies |
| **Markdown** | marked.js | Rich text rendering |
| **Sanitization** | DOMPurify | XSS protection |
| **Math** | KaTeX | LaTeX equation rendering |
| **Code Highlighting** | highlight.js | Syntax highlighting |
| **Icons** | Phosphor Icons | Modern icon set |
| **Styling** | Custom CSS | Design tokens, CSS variables |

### Development
- **Python**: 3.13+
- **Language Composition**: Python 39.2% | HTML 60.8%
- **Testing**: FastAPI TestClient
- **Logging**: Python logging with custom formatters

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Web Interface (HTML/CSS/JS)                       │
│  - Login/Register UI      - Chat Interface      - File Upload       │
│  - Conversation Sidebar   - Markdown Rendering  - Real-time Stream  │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                │ HTTPS/REST API
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FastAPI Application Server                       │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  API Endpoints                                                │  │
│  │  /api/v1/auth/*       - Authentication (login, register)     │  │
│  │  /api/v1/upload       - Document upload                      │  │
│  │  /api/v1/query        - Synchronous Q&A                      │  │
│  │  /api/v1/query-stream - Streaming Q&A (SSE)                  │  │
│  │  /api/v1/history/*    - Conversation management              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Middleware & Security                                        │  │
│  │  - JWT Token Validation  - CORS Headers  - Error Handling    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  SQLite Database │   │  Services Layer  │   │  ChromaDB Vector │
│                  │   │                  │   │      Store       │
│  - Users         │   │  - Ingestion     │   │                  │
│  - Conversations │   │  - Retrieval     │   │  - Documents     │
│  - Messages      │   │  - Generation    │   │  - Embeddings    │
│                  │   │  - History       │   │  - Metadata      │
└──────────────────┘   └──────────────────┘   └──────────────────┘
                                │
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   External Services     │
                    │                         │
                    │  - NVIDIA API (LLM)     │
                    │  - HuggingFace (Models) │
                    └─────────────────────────┘
```

### Data Flow: Query Processing

```
User Query → JWT Validation → Load/Create Conversation
    ↓
Contextualize Query (History-Aware)
    ↓
Hybrid Retrieval (BM25 + Vector) → Top 10 Results
    ↓
Rerank with FlashRank → Top 5 Results
    ↓
Generate Answer (LLM + Context) → Stream Response (SSE)
    ↓
Persist to History → Update Conversation
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** installed ([Download](https://www.python.org/downloads/))
- **pip** package manager
- **NVIDIA API Key** for GPT-OSS-20B ([Get Free Key](https://build.nvidia.com/))
- **Git** for cloning the repository

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/Draxer542/SourceOne.git
cd SourceOne
```

2. **Create Virtual Environment**

```bash
# Using venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### First Run

1. **Create Environment File**

```bash
# Copy the example (if provided) or create new .env
touch .env
```

2. **Add Configuration** (Edit `.env`)

```env
# Required: NVIDIA API Key
NVIDIA_API_KEY=your_nvidia_api_key_here

# Optional: Customize these
SECRET_KEY=your_secret_key_for_jwt_signing
LOG_LEVEL=INFO
CHROMA_DB_DIR=data/chroma_db
```

3. **Start the Server**

```bash
# Development mode (with auto-reload)
python app/main.py

# Or using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. **Access the Application**

- **Web Interface**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

### Your First Interaction

1. **Register an Account**: Click "Sign up" on the login page
2. **Upload Documents**: Use the paperclip icon to upload PDF/TXT/MD/DOCX files (max 3)
3. **Ask Questions**: Type your query and press Enter or click Send
4. **View History**: Access past conversations in the left sidebar

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NVIDIA_API_KEY` | *Required* | API key for NVIDIA NIM/LLM access |
| `SECRET_KEY` | Auto-generated | JWT signing secret (change in production!) |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration time |
| `LOG_LEVEL` | `INFO` | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `CHROMA_DB_DIR` | `data/chroma_db` | Vector database storage path |
| `GOOGLE_API_KEY` | *(Optional)* | Google API key (if using Gemini) |
| `OPENAI_API_KEY` | *(Optional)* | OpenAI key (for alternative models) |

### Application Settings

Edit `app/core/config.py` to modify:

```python
class Settings(BaseSettings):
    # Chunking parameters
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Retrieval settings
    TOP_K: int = 10
    RERANK_TOP_N: int = 5
    
    # Generation settings
    LLM_TEMPERATURE: float = 0.5
    MAX_TOKENS: int = 2000
```

### Database Initialization

On first run, SQLAlchemy automatically creates:
- `data/auth.db` - User accounts and conversations

To reset the database:
```bash
rm data/auth.db
# Restart the server to recreate
```

---

## 💡 Usage Guide

### Authentication Flow

#### Register New User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true
}
```

#### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=SecurePass123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Document Upload

```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "files=@document1.pdf" \
  -F "files=@document2.txt"
```

Response:
```json
{
  "message": "Successfully processed 2 files into 45 chunks."
}
```

### Query (Synchronous)

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main findings?",
    "conversation_id": 1
  }'
```

Response:
```json
{
  "answer": "Based on the documents, the main findings include...",
  "source_documents": [
    {
      "content": "Document excerpt...",
      "metadata": {
        "source": "document1.pdf",
        "page": 3
      }
    }
  ],
  "conversation_id": 1
}
```

### Query (Streaming)

```bash
curl -X POST "http://localhost:8000/api/v1/query-stream" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain the methodology"
  }' \
  --no-buffer
```

Response (Server-Sent Events):
```
event: session
data: {"conversation_id": 2}

data: "Based"

data: " on"

data: " the"

data: " documents..."

event: sources
data: [{"source":"doc.pdf","page":5}]

event: done
data: [DONE]
```

### Conversation History

#### List Conversations
```bash
curl -X GET "http://localhost:8000/api/v1/history/conversations?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Get Conversation Details
```bash
curl -X GET "http://localhost:8000/api/v1/history/conversations/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Delete Conversation
```bash
curl -X DELETE "http://localhost:8000/api/v1/history/conversations/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Create new user account | No |
| POST | `/auth/login` | Authenticate and get JWT token | No |

### Document Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/upload` | Upload documents (PDF, MD, TXT, DOCX) | Yes |

### Query Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/query` | Synchronous Q&A | Yes |
| POST | `/query-stream` | Streaming Q&A (SSE) | Yes |

### History Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/history/conversations` | List user's conversations | Yes |
| POST | `/history/conversations` | Create new conversation | Yes |
| GET | `/history/conversations/{id}` | Get conversation details | Yes |
| DELETE | `/history/conversations/{id}` | Delete conversation | Yes |

### Request/Response Schemas

#### QueryRequest
```json
{
  "query": "string",
  "conversation_id": "integer (optional)"
}
```

#### QueryResponse
```json
{
  "answer": "string",
  "source_documents": [
    {
      "content": "string",
      "metadata": {
        "source": "string",
        "page": "integer"
      }
    }
  ],
  "conversation_id": "integer"
}
```

For full interactive documentation, visit: http://localhost:8000/docs

---

## 📁 Project Structure

```
SourceOne/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app entry point & lifespan
│   │
│   ├── api/                         # API layer
│   │   ├── auth.py                  # Authentication endpoints
│   │   ├── routes.py                # Document & query endpoints
│   │   ├── history.py               # Conversation history endpoints
│   │   └── schemas.py               # Pydantic request/response models
│   │
│   ├── core/                        # Core configuration
│   │   ├── config.py                # Environment variables & settings
│   │   ├── database.py              # SQLAlchemy setup
│   │   ├── security.py              # JWT & password hashing
│   │   └── logging.py               # Logging configuration
│   │
│   ├── models.py                    # SQLAlchemy ORM models
│   │                                # (User, Conversation, Message)
│   │
│   ├── services/                    # Business logic layer
│   │   ├── embeddings_service.py    # Singleton embeddings model
│   │   ├── ingestion_service.py     # Document processing
│   │   ├── retrieval_service.py     # Hybrid search & reranking
│   │   ├── generation_service.py    # LLM answer generation
│   │   └── history_service.py       # Conversation CRUD operations
│   │
│   └── static/                      # Frontend assets
│       ├── index.html               # Single-page application
│       └── SourceOneLogo.png        # Application logo
│
├── data/                            # Persistent storage (gitignored)
│   ├── chroma_db/                   # ChromaDB vector store
│   └── auth.db                      # SQLite user database
│
├── opt/                             # Model cache (gitignored)
│   └── sentence-transformers/       # Cached embeddings model
│
├── tests/
│   └── test_pipeline.py             # Integration tests
│
├── .env                             # Environment variables (gitignored)
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
├── .python-version                  # Python version (3.13)
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project metadata
├── README.md                        # This file
└── LICENSE                          # MIT License
```

---

## 🔥 Advanced Features

### Context-Aware Query Reformulation

SourceOne automatically reformulates user queries based on conversation history:

```python
# User's conversation history:
# User: "What is RAG?"
# AI: "RAG stands for Retrieval-Augmented Generation..."
# User: "How does it work?" ← Ambiguous!

# SourceOne reformulates to:
# "How does Retrieval-Augmented Generation work?"
```

This happens via LangChain's history-aware retrieval pattern:
```python
context_prompt = ChatPromptTemplate.from_messages([
    ("system", "Reformulate the question to be standalone"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])
```

### Lazy Model Loading

To optimize startup time:
```python
# Embeddings model (90MB) loads on first use
def get_embeddings():
    global _embeddings_instance
    if _embeddings_instance is None:
        _embeddings_instance = HuggingFaceEmbeddings(...)
    return _embeddings_instance
```

### Hybrid Search Strategy

Combines two complementary approaches:

1. **BM25 (Keyword Search)**:
   - Statistical ranking (Okapi BM25)
   - Fast lexical matching
   - Good for exact terms, acronyms

2. **Vector Similarity (Semantic Search)**:
   - Embedding-based cosine similarity
   - Understands meaning, not just words
   - Handles synonyms, paraphrasing

```python
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5]  # Equal contribution
)
```

### FlashRank Reranking

After hybrid retrieval (10 results), FlashRank cross-encoder reranks:
```python
# Input: Query + 10 Documents
# Output: 5 Most Relevant Documents
# Model: ms-marco-MiniLM-L-12-v2 (42MB)
```

This two-stage approach balances speed (cheap retrieval) and quality (expensive reranking).

### Real-Time Streaming with SSE

Server-Sent Events enable instant feedback:

```javascript
// Frontend listens to SSE stream
const response = await fetch('/api/v1/query-stream', {...});
const reader = response.body.getReader();

while (true) {
  const {done, value} = await reader.read();
  if (done) break;
  
  // Parse SSE events
  if (line.startsWith('data:')) {
    const chunk = JSON.parse(line.slice(6));
    displayChunk(chunk);  // Update UI in real-time
  }
}
```

### Markdown + LaTeX Rendering

Math protection system prevents markdown from breaking LaTeX:
```javascript
// 1. Protect math expressions
const protected = MathProtector.protect(text);
// $$ E = mc^2 $$ → MATHBLOCK0z

// 2. Render markdown
const html = marked.parse(protected);

// 3. Restore math
const restored = MathProtector.restore(html);
// MATHBLOCK0z → $$ E = mc^2 $$

// 4. Render with KaTeX
renderMathInElement(container);
```

---

## 🐳 Deployment

### Using Docker (Coming Soon)

```dockerfile
# Dockerfile example
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml example
version: '3.8'

services:
  sourceone:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NVIDIA_API_KEY=${NVIDIA_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./data:/app/data
      - ./opt:/app/opt
```

### Production Deployment

1. **Set Secure Secret Key**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Use output as SECRET_KEY in .env
```

2. **Use Production Server**:
```bash
# Install Gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

3. **Add Reverse Proxy** (Nginx example):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # SSE streaming support
        proxy_buffering off;
        proxy_cache off;
    }
}
```

4. **Enable HTTPS** with Let's Encrypt:
```bash
sudo certbot --nginx -d your-domain.com
```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs**: [Open an issue](https://github.com/Draxer542/SourceOne/issues/new?template=bug_report.md)
- 💡 **Suggest Features**: [Request a feature](https://github.com/Draxer542/SourceOne/issues/new?template=feature_request.md)
- 📝 **Improve Documentation**: Fix typos, add examples, clarify explanations
- 🔧 **Submit Code**: Fix bugs, add features, optimize performance
- 🎨 **Enhance UI/UX**: Improve design, add animations, increase accessibility

### Development Setup

1. **Fork the Repository**
```bash
gh repo fork Draxer542/SourceOne --clone
cd SourceOne
```

2. **Create Feature Branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Make Changes**
- Follow PEP 8 style guide
- Add docstrings to functions
- Update tests if needed
- Run tests: `python -m pytest tests/`

4. **Commit & Push**
```bash
git add .
git commit -m "feat: add amazing feature"
git push origin feature/amazing-feature
```

5. **Open Pull Request**
- Provide clear description
- Reference related issues
- Wait for review

### Code Style

```python
# Good: Clear function with docstring
def contextualize_query(query: str, history: List[BaseMessage]) -> str:
    """
    Rewrite user query into standalone question using conversation history.
    
    Args:
        query: User's original question
        history: Prior conversation messages
    
    Returns:
        Standalone query that incorporates context
    """
    # Implementation...
```

### Commit Conventions

Use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ JWT Authentication
- ✅ Conversation History
- ✅ Hybrid Search (BM25 + Vector)
- ✅ FlashRank Reranking
- ✅ SSE Streaming
- ✅ Markdown + LaTeX Rendering

### Version 1.1 (Planned)
- [ ] **Multi-tenancy**: Tenant isolation with per-tenant vector stores
- [ ] **Document Management**: Edit, delete, version documents
- [ ] **Advanced Analytics**: Query metrics, usage dashboards
- [ ] **Export Conversations**: Download chat history as PDF/Markdown

### Version 2.0 (Future)
- [ ] **Multi-modal Support**: Image uploads, OCR, vision models
- [ ] **Custom Models**: Support for Llama, Mistral, Claude
- [ ] **Vector Database Options**: Pinecone, Weaviate, Qdrant
- [ ] **Elasticsearch Integration**: Advanced full-text search
- [ ] **Rate Limiting**: API throttling, usage quotas
- [ ] **Webhooks**: External integrations, notifications
- [ ] **Collaboration**: Shared workspaces, team features

### Enterprise Features (Roadmap)
- [ ] SSO/SAML Integration
- [ ] RBAC (Role-Based Access Control)
- [ ] Audit Logs
- [ ] Data Encryption at Rest
- [ ] GDPR Compliance Tools (right to be forgotten)
- [ ] On-Premise Deployment

Vote on features: [GitHub Discussions](https://github.com/Draxer542/SourceOne/discussions)

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Draxer542

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

See [LICENSE](LICENSE) file for full details.

---

## 💬 Support

### Get Help

- 📖 **Documentation**: Check this README and [API Docs](http://localhost:8000/docs)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Draxer542/SourceOne/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/Draxer542/SourceOne/discussions)
- 📧 **Email**: draxertechupdates@gmail.com

### Community

- ⭐ **Star the Repo**: Show your support!
- 🍴 **Fork & Contribute**: Help make SourceOne better
- 🐦 **Share**: Spread the word about SourceOne

### Acknowledgments

Built with amazing open-source technologies:

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [LangChain](https://www.langchain.com/) - LLM application framework
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [HuggingFace](https://huggingface.co/) - Transformers & embeddings
- [FlashRank](https://github.com/PrithivirajDamodaran/FlashRank) - Lightning-fast reranking
- [NVIDIA NIM](https://build.nvidia.com/) - LLM inference platform

---
    
  [⬆ Back to Top](#sourceone)
  
