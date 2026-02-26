"""Generated-compatible Python stubs for model_lifecycle.proto.

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


class ModelLifecycleAction(IntEnum):
    """Enum for model lifecycle actions."""

    MODEL_LIFECYCLE_ACTION_UNSPECIFIED = 0
    MODEL_REGISTERED = 1
    MODEL_TRAINING_STARTED = 2
    MODEL_TRAINING_COMPLETED = 3
    MODEL_VALIDATION_PASSED = 4
    MODEL_VALIDATION_FAILED = 5
    MODEL_DEPLOYED = 6
    MODEL_UNDEPLOYED = 7
    MODEL_ARCHIVED = 8
    MODEL_DELETED = 9


@dataclass
class ModelLifecycleEvent:
    """Event representing a change in model lifecycle state."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    model_id: str = ""
    model_name: str = ""
    version: str = ""
    action: ModelLifecycleAction = ModelLifecycleAction.MODEL_LIFECYCLE_ACTION_UNSPECIFIED
    triggered_by: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else int(v) if isinstance(v, ModelLifecycleAction) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "ModelLifecycleEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        if "action" in parsed and isinstance(parsed["action"], int):
            parsed["action"] = ModelLifecycleAction(parsed["action"])
        return cls(**parsed)
