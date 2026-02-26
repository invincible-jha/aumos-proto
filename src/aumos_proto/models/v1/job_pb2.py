"""Generated-compatible Python stubs for job.proto.

These are Python dataclass implementations mirroring the Protobuf definitions.
In production, these will be replaced by actual protoc-generated code.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from typing import Any


class JobStatus(IntEnum):
    """Enum for async job execution status."""

    JOB_STATUS_UNSPECIFIED = 0
    PENDING = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4
    CANCELLED = 5


@dataclass
class Job:
    """Job represents an async task submitted to AumOS for execution."""

    id: str = ""
    tenant_id: str = ""
    job_type: str = ""
    status: JobStatus = JobStatus.JOB_STATUS_UNSPECIFIED
    input_params: dict[str, Any] = field(default_factory=dict)
    output: dict[str, Any] = field(default_factory=dict)
    created_by: str = ""
    progress_percent: float = 0.0
    error_message: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: datetime | None = None
    completed_at: datetime | None = None

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (
                v.isoformat() if isinstance(v, datetime)
                else int(v) if isinstance(v, JobStatus)
                else v
            )
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "Job":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        for time_field in ("created_at", "started_at", "completed_at"):
            if time_field in parsed and isinstance(parsed[time_field], str):
                parsed[time_field] = datetime.fromisoformat(parsed[time_field])
        if "status" in parsed and isinstance(parsed["status"], int):
            parsed["status"] = JobStatus(parsed["status"])
        return cls(**parsed)
