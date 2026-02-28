"""Python stubs for resilience_event.proto.

These dataclass implementations mirror the Protobuf definitions and provide
SerializeToString() / FromString() compatibility with the betterproto API.
Replace with real protoc-generated output once buf generate pipeline is active.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class CircuitBreakerEvent:
    """Records state transitions in a circuit breaker."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    circuit_name: str = ""
    from_state: str = ""   # closed, open, half_open
    to_state: str = ""
    source_service: str = ""
    failure_count: int = 0
    success_count: int = 0
    trigger_reason: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "CircuitBreakerEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        return cls(**parsed)


@dataclass
class RateLimitEvent:
    """Records when a rate limit threshold is crossed."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    path: str = ""
    limit: int = 0
    current_count: int = 0
    rejected: bool = False
    source_service: str = ""
    client_id: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "RateLimitEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        return cls(**parsed)


@dataclass
class BulkheadEvent:
    """Records when a bulkhead rejects a call due to concurrency saturation."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    bulkhead_name: str = ""
    max_concurrent_calls: int = 0
    active_calls: int = 0
    rejected: bool = False
    source_service: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "BulkheadEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        return cls(**parsed)
