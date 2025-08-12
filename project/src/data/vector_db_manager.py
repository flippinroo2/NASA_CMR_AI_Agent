from typing import Any

import chromadb
import chromadb.api
import langchain_chroma
import langchain_core.embeddings

# import langchain_ollama.embeddings


class VectorDBManager:
    chroma_client: chromadb.api.ClientAPI
    embeddings_model: langchain_core.embeddings.Embeddings
    vector_store: langchain_chroma.Chroma

    def __init__(self):
        self.chroma_client = chromadb.Client()

    def create_vector_store(self, collection_name: str, embeddings: langchain_core.embeddings.Embeddings):
        self.set_vector_store(
            langchain_chroma.Chroma(collection_name=collection_name, embedding_function=embeddings)
        )

    def get_vector_store(self):
        return self.vector_store

    def set_vector_store(self, vector_store: langchain_chroma.Chroma):
        self.vector_store = vector_store

    def get_embeddings_model(self):
        return self.embeddings_model

    def set_embeddings_model(self, embeddings_model: langchain_core.embeddings.Embeddings):
        self.embeddings_model = embeddings_model

    def retrieve_relevant_context(self, state: dict[str, Any]) -> dict[str, Any]:
        query = state["query"]
        # Perform vector similarity search
        documents = self.vector_store.similarity_search(query, k=3)
        # Add retrieved documents to state
        state["context"] = [doc.page_content for doc in documents]
        return state
