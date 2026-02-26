"""Generated-compatible Python stubs for security_alert.proto.

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


class AlertSeverity(IntEnum):
    """Enum for security alert severity levels."""

    ALERT_SEVERITY_UNSPECIFIED = 0
    INFO = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


@dataclass
class SecurityAlertEvent:
    """Event representing a security alert or threat detection."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    severity: AlertSeverity = AlertSeverity.ALERT_SEVERITY_UNSPECIFIED
    alert_type: str = ""
    source_service: str = ""
    description: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    affected_resources: list[str] = field(default_factory=list)
    mitigation_action: str = ""
    auto_mitigated: bool = False
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else int(v) if isinstance(v, AlertSeverity) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "SecurityAlertEvent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        if "severity" in parsed and isinstance(parsed["severity"], int):
            parsed["severity"] = AlertSeverity(parsed["severity"])
        return cls(**parsed)
