from typing import Any

import chromadb
from chromadb.api import ClientAPI
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_ollama.embeddings import OllamaEmbeddings
from langgraph.graph import END, StateGraph

# from pydantic import BaseModel


class VectorDBManager:
    chroma_client: ClientAPI
    embeddings_model: Embeddings
    vector_store: Chroma

    def __init__(self):
        self.chroma_client = chromadb.Client()

    def create_vector_store(self, collection_name: str, embeddings: Embeddings):
        self.set_vector_store(
            Chroma(collection_name=collection_name, embedding_function=embeddings)
        )

    def get_vector_store(self):
        return self.vector_store

    def set_vector_store(self, vector_store: Chroma):
        self.vector_store = vector_store

    def get_embeddings_model(self):
        return self.embeddings_model

    def set_embeddings_model(self, embeddings_model: Embeddings):
        self.embeddings_model = embeddings_model

    def retrieve_relevant_context(self, state: dict[str, Any]) -> dict[str, Any]:
        query = state["query"]
        # Perform vector similarity search
        documents = self.vector_store.similarity_search(query, k=3)
        # Add retrieved documents to state
        state["context"] = [doc.page_content for doc in documents]
        return state
