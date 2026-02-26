"""Generated-compatible Python stubs for tenant.proto.

These are Python dataclass implementations mirroring the Protobuf definitions.
In production, these will be replaced by actual protoc-generated code.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum


class TenantStatus(IntEnum):
    """Enum for tenant lifecycle status."""

    TENANT_STATUS_UNSPECIFIED = 0
    PROVISIONING = 1
    ACTIVE = 2
    SUSPENDED = 3
    DECOMMISSIONED = 4


@dataclass
class TenantQuota:
    """Resource quota assigned to a tenant."""

    cpu_cores: int = 0
    memory_gb: int = 0
    gpu_count: int = 0
    storage_gb: int = 0
    max_models: int = 0


@dataclass
class Tenant:
    """Tenant represents an isolated organizational unit within AumOS."""

    id: str = ""
    name: str = ""
    display_name: str = ""
    status: TenantStatus = TenantStatus.TENANT_STATUS_UNSPECIFIED
    tier: str = ""
    k8s_namespace: str = ""
    quota: TenantQuota = field(default_factory=TenantQuota)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data: dict = {}
        for k, v in self.__dict__.items():
            if isinstance(v, datetime):
                data[k] = v.isoformat()
            elif isinstance(v, TenantStatus):
                data[k] = int(v)
            elif isinstance(v, TenantQuota):
                data[k] = v.__dict__
            else:
                data[k] = v
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "Tenant":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        for time_field in ("created_at", "updated_at"):
            if time_field in parsed and isinstance(parsed[time_field], str):
                parsed[time_field] = datetime.fromisoformat(parsed[time_field])
        if "status" in parsed and isinstance(parsed["status"], int):
            parsed["status"] = TenantStatus(parsed["status"])
        if "quota" in parsed and isinstance(parsed["quota"], dict):
            parsed["quota"] = TenantQuota(**parsed["quota"])
        return cls(**parsed)
