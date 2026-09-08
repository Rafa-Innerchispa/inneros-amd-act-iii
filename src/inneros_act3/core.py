from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Literal

Target = Literal['amd-local', 'amd-cloud']


@dataclass(frozen=True)
class RouteRequest:
    privacy_required: bool = False
    local_available: bool = True
    cloud_available: bool = True
    needs_elastic_capacity: bool = False
    latency_sensitive: bool = False


@dataclass(frozen=True)
class RoutingEvidence:
    target: Target
    reason_codes: tuple[str, ...]
    policy: str = 'local-first-v1'

    def canonical_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(',', ':'))

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_json().encode('utf-8')).hexdigest()


def route(req: RouteRequest) -> RoutingEvidence:
    reasons: list[str] = []
    if req.privacy_required:
        if not req.local_available:
            raise RuntimeError('privacy policy requires local execution but local target is unavailable')
        reasons.append('privacy')
        return RoutingEvidence('amd-local', tuple(reasons))

    if req.needs_elastic_capacity and req.cloud_available:
        reasons.append('capability')
        return RoutingEvidence('amd-cloud', tuple(reasons))

    if req.local_available:
        reasons.append('local_first')
        if req.latency_sensitive:
            reasons.append('latency')
        return RoutingEvidence('amd-local', tuple(reasons))

    if req.cloud_available:
        reasons.extend(['availability', 'fallback'])
        return RoutingEvidence('amd-cloud', tuple(reasons))

    raise RuntimeError('no execution target available')


def verify_evidence(evidence: RoutingEvidence, expected_sha256: str) -> bool:
    return evidence.sha256() == expected_sha256
