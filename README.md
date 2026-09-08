# mini-rag

RAG (Retrieval-Augmented Generation) pipeline sederhana menggunakan [OpenRouter](https://openrouter.ai) sebagai gateway LLM/embedding dan [ChromaDB](https://www.trychroma.com) sebagai vector database lokal.

## Instalasi

```bash
pip install mini-rag-openrouter
```

Untuk contoh REST API (FastAPI), install dengan extra `api`:

```bash
pip install "mini-rag[api]"
```

## Pemakaian Cepat

```python
from mini_rag import RAGPipeline

rag = RAGPipeline(
    api_key="sk-or-xxxxxxxx",   # API key dari openrouter.ai
    chroma_path="./chroma_db",  # lokasi penyimpanan vector database
)

# Ingest dokumen dari folder (mendukung .txt, .pdf, .docx)
rag.ingest_folder("./dokumen")

# Tanya
result = rag.query("Apa itu ChromaDB?")
print(result["answer"])
print(result["sources"])
```

## Fitur

- Ingest dokumen `.txt`, `.pdf`, `.docx` dari satu folder sekaligus
- Deteksi dokumen yang sudah pernah di-ingest (skip otomatis, hemat API call)
- Vector search lokal via ChromaDB, tidak perlu server tambahan
- Model embedding & chat bisa dikustomisasi lewat parameter

## Kustomisasi Model

```python
rag = RAGPipeline(
    api_key="sk-or-xxxxxxxx",
    embed_model="cohere/embed-v4",
    chat_model="anthropic/claude-sonnet-4.6",
)
```

## Contoh REST API

Lihat `examples/app.py` untuk contoh integrasi ke FastAPI (endpoint `/ingest` dan `/query`).

```bash
cd examples
cp .env.example .env   # isi OPENROUTER_API_KEY
uvicorn app:app --reload
```

## Lisensi

MIT