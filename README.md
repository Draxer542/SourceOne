# SourceOne

A comprehensive Retrieval-Augmented Generation (RAG) system built with FastAPI, LangChain, ChromaDB, and OpenAI. This project enables users to upload documents, perform intelligent retrieval using hybrid search and reranking, and generate context-aware responses using large language models.

## Features

- **Document Ingestion**: Upload and process multiple file types (PDF, Markdown, TXT, DOCX) with automatic text splitting and embedding.
- **Hybrid Retrieval**: Combines BM25 keyword search with semantic vector search for optimal document retrieval.
- **Reranking**: Uses FlashRank to improve retrieval quality by reranking results based on relevance.
- **LLM Generation**: Leverages GPT-OSS 120B for generating accurate, context-aware answers with streaming support.
- **Advanced UI/UX**:
  - Real-time streaming responses with "Thinking..." indicators
  - LaTeX math rendering with KaTeX (supports `$$`, `\[`, and `[` delimiters)
  - Syntax-highlighted code blocks with copy-to-clipboard functionality
  - Source citations displayed with each answer
  - Responsive design with modern aesthetics
- **Performance Optimizations**:
  - Lazy-loaded embeddings model for faster startup
  - Non-blocking file uploads with background indexing
  - JSON-encoded SSE streaming for preserved formatting
- **REST API**: Full REST API for integration with other applications.
- **Persistent Storage**: ChromaDB for efficient vector storage and retrieval.
- **Debug Tools**: Included scripts for debugging retrieval, generation, and search comparison.

## Installation

### Prerequisites

- Python 3.13 or higher
- Google Cloud API key with access to OpenAI models

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/agenticrag.git
   cd agenticrag
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your configuration:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   LOG_LEVEL=INFO
   CHROMA_DB_DIR=data/chroma_db
   ```

## Configuration

The application uses the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key for accessing OpenAI models (required)
- `LOG_LEVEL`: Logging level (default: INFO)
- `CHROMA_DB_DIR`: Directory for ChromaDB persistence (default: data/chroma_db)

## Usage

### Running the Application

Start the FastAPI server:

```bash
python app/main.py
```

The application will be available at:

- Web UI: http://localhost:8000
- API Documentation: http://localhost:8000/docs (Swagger UI)

### Using the Web Interface

1. Open http://localhost:8000 in your browser
2. Upload documents using the upload section (supports PDF, MD, TXT, DOCX files, max 3 files)
3. Enter your query in the query section
4. View the generated answer along with source documents

### Using the API

#### Upload Documents

```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "files=@document1.pdf" \
  -F "files=@document2.txt"
```

#### Query the System

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the main topic of the documents?"}'
```

## API Documentation

### Endpoints

#### POST /api/v1/upload

Upload and process documents.

**Request:**

- `files`: List of files (PDF, MD, TXT, DOCX)

**Response:**

```json
{
  "message": "Files processed successfully"
}
```

#### POST /api/v1/query

Query the RAG system.

**Request:**

```json
{
  "query": "Your question here"
}
```

**Response:**

```json
{
  "answer": "Generated answer based on retrieved documents",
  "source_documents": [
    {
      "content": "Document content snippet",
      "metadata": {
        "source": "filename.pdf",
        "page": 1
      }
    }
  ]
}
```

#### POST /api/v1/query-stream

Query the RAG system with streaming response.

**Request:**

```json
{
  "query": "Your question here"
}
```

**Response:**

Server-Sent Events (SSE) stream with:

- `data:` events containing answer chunks (JSON-encoded)
- `event: sources` with source document metadata
- `data: [DONE]` to signal completion

## Project Structure

```
agenticrag/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── routes.py        # API endpoints
│   │   └── schemas.py       # Pydantic models
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   └── logging.py       # Logging configuration
│   ├── services/
│   │   ├── embeddings_service.py   # Singleton embeddings model
│   │   ├── ingestion_service.py    # Document ingestion
│   │   ├── retrieval_service.py    # Document retrieval
│   │   └── generation_service.py   # Answer generation
│   └── static/
│       └── index.html       # Web interface
├── data/
│   └── chroma_db/           # ChromaDB storage
├── opt/                     # Model files
├── debug_*.py               # Debug scripts
├── test_pipeline.py         # Pipeline testing
├── pyproject.toml           # Project configuration
├── requirements.txt         # Python dependencies
└── README.md
```

## Architecture

The system follows a modular architecture with three main services:

1. **Ingestion Service**: Handles document upload, parsing, chunking, and embedding storage
2. **Retrieval Service**: Performs hybrid search (BM25 + vector similarity) and reranking
3. **Generation Service**: Uses retrieved context to generate answers via LLM

## Debug and Testing

The project includes several debug and testing scripts:

- `debug_retrieval.py`: Test document retrieval functionality
- `debug_generation.py`: Test answer generation
- `debug_chroma.py`: Debug ChromaDB operations
- `compare_search.py`: Compare different search methods
- `test_pipeline.py`: End-to-end pipeline testing

Run any debug script:

```bash
python debug_retrieval.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [LangChain](https://www.langchain.com/)
- Vector storage with [ChromaDB](https://www.trychroma.com/)
- Reranking with [FlashRank](https://github.com/PrithivirajDamodaran/FlashRank)
