"""
Type C: Retrieval Traces adapter (STUB).

In production this connects to the vector store (Pinecone, Weaviate, Qdrant,
pgvector) or the RAG framework's trace store (LangChain callbacks, LlamaIndex
trace store, custom retrieval logging). The PB03 seven-component pipeline
forensics live here.

The stub returns 3 synthetic records demonstrating per-query retrieval results.
"""
from __future__ import annotations


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    return [
        {
            "record_id": f"{incident_id}-c-001",
            "timestamp": "2026-06-29T14:12:34Z",
            "query_text_hash": "sha256:abc" + "0" * 61,
            "corpus_id": "salesforce-opportunity-notes",
            "corpus_version": "v2026-06-28",
            "embedding_model": "text-embedding-3-small",
            "retrieved_documents": [
                {"doc_id": "doc-001", "version": "v3", "similarity_score": 0.87},
                {"doc_id": "doc-002", "version": "v1", "similarity_score": 0.81},
                {"doc_id": "doc-003", "version": "v2", "similarity_score": 0.74},
            ],
            "top_k": 5,
            "reranker_applied": True,
        },
        {
            "record_id": f"{incident_id}-c-002",
            "timestamp": "2026-06-29T14:14:02Z",
            "query_text_hash": "sha256:def" + "0" * 61,
            "corpus_id": "internal-runbooks",
            "corpus_version": "v2026-06-15",
            "embedding_model": "text-embedding-3-small",
            "retrieved_documents": [
                {"doc_id": "runbook-042", "version": "v1", "similarity_score": 0.92},
            ],
            "top_k": 5,
            "reranker_applied": False,
        },
        {
            "record_id": f"{incident_id}-c-003",
            "timestamp": "2026-06-29T14:18:18Z",
            "query_text_hash": "sha256:abc" + "0" * 61,
            "corpus_id": "salesforce-opportunity-notes",
            "corpus_version": "v2026-06-28",
            "embedding_model": "text-embedding-3-small",
            "retrieved_documents": [
                {"doc_id": "doc-019-EXTERNAL-VENDOR-NOTE", "version": "v1", "similarity_score": 0.79},
            ],
            "top_k": 5,
            "reranker_applied": True,
            "note": "Possible workflow-injection vector per PB06; doc-019 originated from external email-to-CRM pipeline",
        },
    ]
