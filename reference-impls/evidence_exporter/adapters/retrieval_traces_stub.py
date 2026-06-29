"""
Type C: Retrieval Traces adapter (STUB).

Spec field requirements (per schemas/evidence-export.spec.md line 92):
  {timestamp, query, corpus_id, documents_retrieved: [{doc_id, version,
   similarity_score, chunk_index}], reranker_version, top_k_setting,
   filters_applied}

Per spec PB03 Type C-extended: each retrieved chunk MUST carry doc_id,
version, and ingestion_timestamp. Embedding model version MUST be captured
because changes affect ranking and are forensically relevant.

In production this connects to the vector store (Pinecone, Weaviate, Qdrant,
pgvector) or the RAG framework's trace store (LangChain callbacks, LlamaIndex
trace store, custom retrieval logging).
"""
from __future__ import annotations


def capture(agent_id: str, window_start: str, window_end: str, incident_id: str) -> list[dict]:
    """Return Type C records in the spec's canonical format."""
    return [
        {
            "timestamp": "2026-06-29T14:12:34.198Z",
            "query": "[STUB: full query text; production redaction per PB23]",
            "corpus_id": "salesforce-opportunity-notes",
            "documents_retrieved": [
                {"doc_id": "doc-001", "version": "v3", "similarity_score": 0.87, "chunk_index": 0},
                {"doc_id": "doc-002", "version": "v1", "similarity_score": 0.81, "chunk_index": 2},
                {"doc_id": "doc-003", "version": "v2", "similarity_score": 0.74, "chunk_index": 0},
            ],
            "reranker_version": "cohere-rerank-3-en-v1.0",
            "top_k_setting": 5,
            "filters_applied": {"corpus_class": "internal_only"},
        },
        {
            "timestamp": "2026-06-29T14:14:02.331Z",
            "query": "[STUB: query about runbook procedures]",
            "corpus_id": "internal-runbooks",
            "documents_retrieved": [
                {"doc_id": "runbook-042", "version": "v1", "similarity_score": 0.92, "chunk_index": 0},
            ],
            "reranker_version": "none",
            "top_k_setting": 5,
            "filters_applied": {},
        },
        {
            "timestamp": "2026-06-29T14:18:18.617Z",
            "query": "[STUB: query with potential injection vector]",
            "corpus_id": "salesforce-opportunity-notes",
            "documents_retrieved": [
                {"doc_id": "doc-019-EXTERNAL-VENDOR-NOTE", "version": "v1", "similarity_score": 0.79, "chunk_index": 0},
            ],
            "reranker_version": "cohere-rerank-3-en-v1.0",
            "top_k_setting": 5,
            "filters_applied": {"corpus_class": "internal_only"},
        },
    ]
