from Backend.vector_store import search_similar_chunks


class RetrieverAgent:
    """
    Retriever Agent:
    - Searches FAISS vector database.
    - Returns best matching chunks and source file.
    """

    def __init__(self, top_k: int = 5):
        self.top_k = top_k

    def run(self, question: str) -> dict:
        retrieved_chunks, source_files = search_similar_chunks(
            question,
            k=self.top_k
        )

        if not retrieved_chunks:
            return {
                "context": "",
                "chunks": [],
                "sources": [],
                "found": False
            }

        context = "\n\n".join(retrieved_chunks)

        return {
            "context": context,
            "chunks": retrieved_chunks,
            "sources": source_files,
            "found": True
        }


retriever_agent = RetrieverAgent()