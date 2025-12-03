import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_sample_files():
    with open("sample.txt", "w") as f:
        f.write("Agentic RAG is a system that uses agents to improve Retrieval Augmented Generation. It involves data ingestion, retrieval, and generation layers.")
    
    with open("sample.md", "w") as f:
        f.write("# Agentic RAG\n\nThis project uses LangChain, FastAPI, and ChromaDB. It supports PDF, MD, TXT, and DOCX files.")

def remove_sample_files():
    if os.path.exists("sample.txt"):
        os.remove("sample.txt")
    if os.path.exists("sample.md"):
        os.remove("sample.md")

def test_upload():
    print("Testing Upload...")
    create_sample_files()
    try:
        with open("sample.txt", "rb") as f1, open("sample.md", "rb") as f2:
            files = [
                ("files", ("sample.txt", f1, "text/plain"))
            ]
            response = client.post("/api/v1/upload", files=files)
            print(f"Upload Response: {response.status_code} - {response.json()}")
            assert response.status_code == 200
    finally:
        remove_sample_files()

def test_query():
    print("Testing Query...")
    query_payload = {"query": "What is Agentic RAG?"}
    response = client.post("/api/v1/query", json=query_payload)
    print(f"Query Response: {response.status_code} - {str(response.json()).encode('utf-8', errors='ignore')}")
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["source_documents"]) > 0

if __name__ == "__main__":
    # Ensure env vars are set or mock them if needed. 
    # For now, we assume .env is present and valid.
    test_upload()
    test_query()
