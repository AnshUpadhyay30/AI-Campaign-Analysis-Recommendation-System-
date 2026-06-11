from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional


class VectorStore:
    """Best-effort local vector memory. Uses Chroma if present, fallback JSON lines otherwise."""

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.fallback_file = self.base_path / "memory.jsonl"
        self._chroma = None
        self._collection = None
        try:
            import chromadb

            client = chromadb.PersistentClient(path=str(base_path))
            self._collection = client.get_or_create_collection(name="agent_memory")
            self._chroma = client
        except Exception:
            self._chroma = None

    def add(self, doc_id: str, text: str, metadata: Optional[dict[str, str]] = None) -> None:
        meta = metadata or {}
        if self._collection is not None:
            self._collection.add(ids=[doc_id], documents=[text], metadatas=[meta])
            return
        record = {"id": doc_id, "text": text, "metadata": meta}
        with self.fallback_file.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")

    def search(self, query: str, top_k: int = 5) -> list[dict[str, str]]:
        if self._collection is not None:
            result = self._collection.query(query_texts=[query], n_results=top_k)
            docs = result.get("documents", [[]])[0]
            metas = result.get("metadatas", [[]])[0]
            return [{"text": d, "metadata": json.dumps(m)} for d, m in zip(docs, metas)]

        if not self.fallback_file.exists():
            return []
        hits: list[dict[str, str]] = []
        with self.fallback_file.open("r", encoding="utf-8") as fh:
            for line in fh:
                obj = json.loads(line)
                text = obj.get("text", "")
                if query.lower() in text.lower():
                    hits.append({"text": text, "metadata": json.dumps(obj.get("metadata", {}))})
        return hits[:top_k]

    def bulk_add(self, rows: Iterable[tuple[str, str, dict[str, str]]]) -> None:
        for doc_id, text, metadata in rows:
            self.add(doc_id, text, metadata)
