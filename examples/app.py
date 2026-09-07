import os
import shutil
import tempfile

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mini_rag import RAGPipeline
from mini_rag.document_loader import load_document

load_dotenv()

rag = RAGPipeline(
    api_key=os.environ["OPENROUTER_API_KEY"],
    chroma_path="./chroma_db",
)

app = FastAPI(title="Mini RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ingest")
async def ingest_endpoint(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        text = load_document(tmp_path)
        rag.ingest_document(text, source_name=file.filename)
    finally:
        os.remove(tmp_path)

    return {"message": f"'{file.filename}' berhasil diproses"}


class QueryRequest(BaseModel):
    question: str


@app.post("/query")
def query_endpoint(request: QueryRequest):
    return rag.query(request.question)