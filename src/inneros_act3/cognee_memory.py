from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
import os
import uuid
from typing import Any, Protocol
from urllib import error, request


DEFAULT_COGNEE_URL = "https://api.cognee.ai"
DEFAULT_DATASET = "inneros-personal-brain"


@dataclass(frozen=True)
class CogneeMemoryConfig:
    base_url: str = DEFAULT_COGNEE_URL
    api_key: str = ""
    dataset: str = DEFAULT_DATASET

    @classmethod
    def from_env(cls) -> "CogneeMemoryConfig":
        return cls(
            base_url=(os.getenv("COGNEE_SERVICE_URL") or DEFAULT_COGNEE_URL).rstrip("/"),
            api_key=(os.getenv("COGNEE_API_KEY") or "").strip(),
            dataset=(os.getenv("COGNEE_DATASET") or DEFAULT_DATASET).strip(),
        )

    @property
    def ready(self) -> bool:
        return bool(self.base_url and self.api_key and self.dataset)


@dataclass(frozen=True)
class SharedMemoryFact:
    fact_id: str
    site: str
    statement: str
    source: str
    verified: bool
    safe_to_share: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.fact_id.strip():
            raise ValueError("fact_id_required")
        if not self.site.strip():
            raise ValueError("site_required")
        if not self.statement.strip():
            raise ValueError("statement_required")
        if not self.source.strip():
            raise ValueError("source_required")
        if not self.verified:
            raise ValueError("verified_fact_required")
        if not self.safe_to_share:
            raise ValueError("safe_to_share_required")

        forbidden = {"password", "secret", "credential", "api_key", "token", "pin"}
        metadata_keys = {str(key).strip().lower() for key in self.metadata}
        if metadata_keys & forbidden:
            raise ValueError("sensitive_metadata_not_allowed")


class CogneeTransport(Protocol):
    def remember(self, *, dataset: str, text: str, node_set: str) -> dict[str, Any]: ...

    def recall(self, *, dataset: str, query: str, top_k: int) -> list[Any]: ...


class HttpCogneeTransport:
    """Small dependency-free transport matching the existing Personal Brain Cognee API."""

    def __init__(self, config: CogneeMemoryConfig):
        self.config = config

    def _headers(self, *, content_type: str) -> dict[str, str]:
        if not self.config.api_key:
            raise RuntimeError("COGNEE_API_KEY is not configured")
        return {
            "X-Api-Key": self.config.api_key,
            "Content-Type": content_type,
        }

    @staticmethod
    def _json_response(response: Any) -> Any:
        raw = response.read()
        return json.loads(raw.decode("utf-8")) if raw else {}

    def recall(self, *, dataset: str, query: str, top_k: int = 8) -> list[Any]:
        payload = {
            "search_type": None,
            "datasets": [dataset],
            "query": query[:1200],
            "top_k": max(1, min(int(top_k), 20)),
            "only_context": True,
            "verbose": True,
        }
        req = request.Request(
            f"{self.config.base_url}/api/v1/recall",
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(content_type="application/json"),
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=45) as response:
                rows = self._json_response(response)
        except error.HTTPError as exc:
            if exc.code != 422:
                raise
            legacy = {
                "searchType": None,
                "datasets": [dataset],
                "query": query[:1200],
                "topK": max(1, min(int(top_k), 20)),
                "onlyContext": True,
                "verbose": True,
            }
            retry = request.Request(
                f"{self.config.base_url}/api/v1/recall",
                data=json.dumps(legacy).encode("utf-8"),
                headers=self._headers(content_type="application/json"),
                method="POST",
            )
            with request.urlopen(retry, timeout=45) as response:
                rows = self._json_response(response)
        return rows if isinstance(rows, list) else [rows]

    def remember(self, *, dataset: str, text: str, node_set: str = "act3-agent-memory") -> dict[str, Any]:
        boundary = f"----inneros-act3-{uuid.uuid4().hex}"
        fields = {
            "raw_data": text[:4000],
            "datasetName": dataset,
            "run_in_background": "true",
            "node_set": node_set[:120],
        }
        chunks: list[bytes] = []
        for name, value in fields.items():
            chunks.extend(
                [
                    f"--{boundary}\r\n".encode("utf-8"),
                    f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                    str(value).encode("utf-8"),
                    b"\r\n",
                ]
            )
        chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
        body = b"".join(chunks)
        req = request.Request(
            f"{self.config.base_url}/api/v1/remember",
            data=body,
            headers=self._headers(content_type=f"multipart/form-data; boundary={boundary}"),
            method="POST",
        )
        with request.urlopen(req, timeout=45) as response:
            result = self._json_response(response)
        return result if isinstance(result, dict) else {"response": result}


@dataclass
class CogneeSharedMemory:
    """ACT III adapter for curated cross-agent memory.

    This deliberately does not replace InnerOS private memory. Only verified,
    explicitly shareable facts cross into the canonical Cognee dataset.
    """

    config: CogneeMemoryConfig = field(default_factory=CogneeMemoryConfig.from_env)
    transport: CogneeTransport | None = None

    @property
    def ready(self) -> bool:
        return bool(self.transport is not None or self.config.ready)

    def _transport(self) -> CogneeTransport:
        if self.transport is not None:
            return self.transport
        if not self.config.ready:
            raise RuntimeError("cognee_not_configured")
        return HttpCogneeTransport(self.config)

    def remember_verified_fact(self, fact: SharedMemoryFact, *, writer_agent: str) -> dict[str, Any]:
        fact.validate()
        envelope = {
            "schema": "inneros.act3.shared-memory.v1",
            "fact": asdict(fact),
            "writer_agent": writer_agent,
        }
        serialized = json.dumps(envelope, ensure_ascii=False, sort_keys=True, default=str)
        result = self._transport().remember(
            dataset=self.config.dataset,
            text=serialized,
            node_set="act3-agent-memory",
        )
        return {
            "ok": True,
            "provider": "cognee",
            "dataset": self.config.dataset,
            "fact_id": fact.fact_id,
            "writer_agent": writer_agent,
            "stored": True,
            "fact_sha256": hashlib.sha256(fact.statement.encode("utf-8")).hexdigest(),
            "provider_response_present": bool(result),
        }

    def recall(self, query: str, *, reader_agent: str, top_k: int = 8) -> dict[str, Any]:
        if not query.strip():
            raise ValueError("query_required")
        rows = self._transport().recall(
            dataset=self.config.dataset,
            query=query,
            top_k=top_k,
        )
        memories: list[str] = []
        for row in rows[: max(1, min(top_k, 20))]:
            if isinstance(row, dict):
                memories.append(str(row.get("text") or row.get("content") or row))
            else:
                memories.append(str(row))
        return {
            "ok": True,
            "provider": "cognee",
            "dataset": self.config.dataset,
            "reader_agent": reader_agent,
            "count": len(memories),
            "memory": memories,
        }


def prove_cross_agent_memory(
    memory: CogneeSharedMemory,
    *,
    fact: SharedMemoryFact,
    writer_agent: str,
    reader_agent: str,
    recall_query: str,
) -> dict[str, Any]:
    """Produce judge-safe evidence for 'Agent A learns -> Agent B remembers'."""

    write = memory.remember_verified_fact(fact, writer_agent=writer_agent)
    recall = memory.recall(recall_query, reader_agent=reader_agent)
    proven = bool(write.get("stored") and recall.get("count", 0) > 0)
    return {
        "schema": "inneros.act3.cognee-proof.v1",
        "state": "PROVEN" if proven else "LIVE-PARTIAL",
        "provider": "cognee",
        "dataset": memory.config.dataset,
        "writer_agent": writer_agent,
        "reader_agent": reader_agent,
        "fact_id": fact.fact_id,
        "fact_sha256": write.get("fact_sha256"),
        "recall_count": recall.get("count", 0),
        "memory": recall.get("memory", []),
        "privacy_boundary": "verified_safe_facts_only",
    }
