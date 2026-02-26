"""Generated-compatible Python stubs for usage_metrics.proto.

These are Python dataclass implementations mirroring the Protobuf definitions.
In production, these will be replaced by actual protoc-generated code.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class UsageMetricsEvent:
    """Event capturing resource usage metrics for billing and monitoring."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    service_name: str = ""
    metric_type: str = ""
    value: float = 0.0
    unit: str = ""
    labels: dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "UsageMetricsEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        return cls(**parsed)
