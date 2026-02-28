"""Python stubs for lock_event.proto.

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
class LockAcquiredEvent:
    """Records when a distributed lock is successfully acquired."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    lock_name: str = ""
    lock_owner: str = ""
    ttl_seconds: int = 0
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
    def FromString(cls, data: bytes) -> "LockAcquiredEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        return cls(**parsed)


@dataclass
class LockReleasedEvent:
    """Records when a distributed lock is released (explicitly or via TTL expiry)."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    lock_name: str = ""
    lock_owner: str = ""
    timed_out: bool = False
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
    def FromString(cls, data: bytes) -> "LockReleasedEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        return cls(**parsed)


@dataclass
class LockContentionEvent:
    """Records when a lock acquisition attempt fails due to contention."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    lock_name: str = ""
    requesting_owner: str = ""
    current_owner: str = ""
    wait_seconds: int = 0
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
    def FromString(cls, data: bytes) -> "LockContentionEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        return cls(**parsed)
