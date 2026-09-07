import chromadb


class VectorStore:
    def __init__(self, chroma_path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=chroma_path)
        self.collection = self.client.get_or_create_collection(name="dokumen_saya")

    def add_chunks(self, chunks: list[str], embeddings: list[list[float]], source_name: str):
        ids = [f"{source_name}-{i}" for i in range(len(chunks))]
        metadatas = [{"source": source_name, "chunk_index": i} for i in range(len(chunks))]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )

    def search_chunks(self, query_embedding: list[float], n_results: int = 4):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        return documents, metadatas

    def is_already_ingested(self, source_name: str) -> bool:
        existing = self.collection.get(where={"source": source_name}, limit=1)
        return len(existing["ids"]) > 0