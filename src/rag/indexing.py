"""Index manager for invoice text embeddings and BM25 token registries."""

from typing import Any, Dict, List


class IndexManager:
    """Manages document chunks, embeddings, and inverted indexes."""

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any]):
        """Index an invoice or policy document."""
        self.documents.append({
            "doc_id": doc_id,
            "content": content,
            "metadata": metadata,
        })
