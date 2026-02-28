"""Python stubs for feature_flag_event.proto.

These dataclass implementations mirror the Protobuf definitions and provide
SerializeToString() / FromString() compatibility with the betterproto API.
Replace with real protoc-generated output once buf generate pipeline is active.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class FeatureFlagEvaluationEvent:
    """Records every evaluation of a feature flag for audit and analytics."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    flag_key: str = ""
    enabled: bool = False
    evaluated_for: str = ""
    source_service: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "FeatureFlagEvaluationEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        return cls(**parsed)


@dataclass
class FeatureFlagChangeEvent:
    """Records updates to feature flag configuration."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    flag_key: str = ""
    previous_enabled: bool = False
    new_enabled: bool = False
    changed_by: str = ""
    change_reason: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "FeatureFlagChangeEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        return cls(**parsed)
