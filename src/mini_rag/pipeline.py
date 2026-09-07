from .chunking import chunk_text
from .embeddings import embed_texts, EMBED_MODEL
from .generation import generate_answer, CHAT_MODEL
from .vector_store import VectorStore
from .document_loader import load_documents_from_folder


class RAGPipeline:
    def __init__(
        self,
        api_key: str,
        chroma_path: str = "./chroma_db",
        embed_model: str = EMBED_MODEL,
        chat_model: str = CHAT_MODEL,
    ):
        self.api_key = api_key
        self.embed_model = embed_model
        self.chat_model = chat_model
        self.vector_store = VectorStore(chroma_path)

    def ingest_document(self, text: str, source_name: str):
        if self.vector_store.is_already_ingested(source_name):
            print(f"Lewati '{source_name}', sudah pernah di-ingest sebelumnya.")
            return

        chunks = chunk_text(text)
        embeddings = embed_texts(chunks, api_key=self.api_key, model=self.embed_model)
        self.vector_store.add_chunks(chunks, embeddings, source_name)
        print(f"Ingested {len(chunks)} chunk dari '{source_name}'")

    def ingest_folder(self, folder_path: str):
        documents = load_documents_from_folder(folder_path)
        for source_name, text in documents:
            self.ingest_document(text, source_name)

    def query(self, question: str) -> dict:
        query_embedding = embed_texts([question], api_key=self.api_key, model=self.embed_model)[0]
        chunks, metadatas = self.vector_store.search_chunks(query_embedding)
        answer = generate_answer(question, chunks, api_key=self.api_key, model=self.chat_model)

        sources = [
            {"source": m["source"], "chunk_index": m["chunk_index"]}
            for m in metadatas
        ]
        return {"answer": answer, "sources": sources}