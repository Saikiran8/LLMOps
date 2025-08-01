from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class RAGEngine:
    def __init__(self):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.embedder = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.vector_db = Chroma(
            persist_directory="db",
            embedding_function=self.embedder
        )
        self.llm = OpenAI(model_name="gpt-4", openai_api_key=openai_api_key)

    def answer(self, query: str, metadata):
        docs = self.vector_db.similarity_search(query, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        prompt = f"Use the context below to answer the question:\n\n{context}\n\nQ: {query}"
        response = self.llm.invoke(prompt)  # invoke() is recommended in latest versions

        doc_ids = [d.metadata.get("doc_id", "unknown") for d in docs]
        metadata.doc_ids = doc_ids
        return response, {
            "used_docs": doc_ids,
            "model_version": metadata.model_version,
        }
