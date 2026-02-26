"""Generated-compatible Python stubs for model.proto.

These are Python dataclass implementations mirroring the Protobuf definitions.
In production, these will be replaced by actual protoc-generated code.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from typing import Any


class ModelStatus(IntEnum):
    """Enum for ML model lifecycle status."""

    MODEL_STATUS_UNSPECIFIED = 0
    DRAFT = 1
    TRAINING = 2
    VALIDATED = 3
    DEPLOYED = 4
    ARCHIVED = 5


@dataclass
class Model:
    """Model represents an ML model artifact managed by AumOS."""

    id: str = ""
    tenant_id: str = ""
    name: str = ""
    version: str = ""
    framework: str = ""
    status: ModelStatus = ModelStatus.MODEL_STATUS_UNSPECIFIED
    artifact_uri: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    created_by: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else int(v) if isinstance(v, ModelStatus) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "Model":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        for time_field in ("created_at", "updated_at"):
            if time_field in parsed and isinstance(parsed[time_field], str):
                parsed[time_field] = datetime.fromisoformat(parsed[time_field])
        if "status" in parsed and isinstance(parsed["status"], int):
            parsed["status"] = ModelStatus(parsed["status"])
        return cls(**parsed)
