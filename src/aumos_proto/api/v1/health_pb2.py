"""Generated-compatible Python stubs for health.proto.

These are Python dataclass implementations mirroring the Protobuf definitions.
In production, these will be replaced by actual protoc-generated code.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ComponentHealth:
    """Health status of a single service component."""

    status: str = ""
    message: str = ""
    latency_ms: float = 0.0

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        return json.dumps(self.__dict__).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "ComponentHealth":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        return cls(**parsed)


@dataclass
class HealthResponse:
    """Aggregated health status response for a service."""

    service: str = ""
    status: str = ""
    version: str = ""
    components: dict[str, ComponentHealth] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data: dict = {}
        for k, v in self.__dict__.items():
            if isinstance(v, datetime):
                data[k] = v.isoformat()
            elif k == "components":
                data[k] = {ck: cv.__dict__ for ck, cv in v.items()}
            else:
                data[k] = v
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "HealthResponse":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        if "components" in parsed and isinstance(parsed["components"], dict):
            parsed["components"] = {
                k: ComponentHealth(**v) for k, v in parsed["components"].items()
            }
        return cls(**parsed)
