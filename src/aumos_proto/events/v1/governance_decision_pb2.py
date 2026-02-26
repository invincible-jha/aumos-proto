"""Generated-compatible Python stubs for governance_decision.proto.

These are Python dataclass implementations mirroring the Protobuf definitions.
In production, these will be replaced by actual protoc-generated code.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from typing import Any


class GovernanceDecision(IntEnum):
    """Enum for governance decision outcomes."""

    GOVERNANCE_DECISION_UNSPECIFIED = 0
    APPROVED = 1
    DENIED = 2
    ESCALATED = 3
    PENDING_REVIEW = 4
    AUTO_APPROVED = 5


@dataclass
class GovernanceDecisionEvent:
    """Event representing a governance policy decision."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    policy_id: str = ""
    policy_name: str = ""
    resource_type: str = ""
    resource_id: str = ""
    decision: GovernanceDecision = GovernanceDecision.GOVERNANCE_DECISION_UNSPECIFIED
    violations: list[str] = field(default_factory=list)
    decided_by: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else int(v) if isinstance(v, GovernanceDecision) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "GovernanceDecisionEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        if "decision" in parsed and isinstance(parsed["decision"], int):
            parsed["decision"] = GovernanceDecision(parsed["decision"])
        return cls(**parsed)
