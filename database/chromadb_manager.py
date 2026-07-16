"""
chromadb_manager.py

Handles:
- Creating ChromaDB collections
- Storing document chunks
- Retrieving similar chunks
- Deleting collections
"""

import chromadb
from chromadb.config import Settings


class ChromaDBManager:

    def __init__(self, collection_name="factorybrain"):

        self.client = chromadb.Client(
            Settings(
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    # ===========================================
    # Add Documents
    # ===========================================

    def add_documents(
        self,
        ids,
        documents,
        embeddings=None,
        metadatas=None
    ):

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(
            f"Added {len(documents)} document(s) to ChromaDB."
        )

    # ===========================================
    # Query Documents
    # ===========================================

    def query(self, query_text, n_results=5):

        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        return results

    # ===========================================
    # Get Collection Info
    # ===========================================

    def get_collection_info(self):

        return {
            "name": self.collection.name,
            "count": self.collection.count()
        }

    # ===========================================
    # Delete Collection
    # ===========================================

    def delete_collection(self):

        self.client.delete_collection(
            self.collection.name
        )

        print(
            f"Collection '{self.collection.name}' deleted."
        )

    # ===========================================
    # List Documents
    # ===========================================

    def list_documents(self):

        return self.collection.get()

    # ===========================================
    # Reset Database
    # ===========================================

    def reset(self):

        self.delete_collection()

        self.collection = self.client.get_or_create_collection(
            name="factorybrain"
        )


# ===========================================
# Demo
# ===========================================

if __name__ == "__main__":

    db = ChromaDBManager()

    docs = [
        "Pump A requires maintenance every 6 months.",
        "Valve X was replaced in Plant 2.",
        "Inspection Report completed successfully."
    ]

    ids = [
        "doc1",
        "doc2",
        "doc3"
    ]

    db.add_documents(
        ids=ids,
        documents=docs
    )

    print("\nCollection Info:")
    print(db.get_collection_info())

    print("\nQuery Results:")
    print(
        db.query(
            "Which pump requires maintenance?"
        )
    )
