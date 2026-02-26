"""Generated-compatible Python stubs for agent_envelope.proto.

These are Python dataclass implementations mirroring the Protobuf definitions.
In production, these will be replaced by actual protoc-generated code.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AgentEnvelope:
    """Standard envelope for all agent-to-agent messages."""

    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    source_agent_id: str = ""
    target_agent_id: str = ""
    conversation_id: str = ""
    message_type: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    privilege_level: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
    ttl_seconds: int = 0
    retry_count: int = 0

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "AgentEnvelope":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "created_at" in parsed and isinstance(parsed["created_at"], str):
            parsed["created_at"] = datetime.fromisoformat(parsed["created_at"])
        return cls(**parsed)
