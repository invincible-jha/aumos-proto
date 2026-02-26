"""Generated-compatible Python stubs for common.proto.

These are Python dataclass implementations mirroring the Protobuf definitions.
In production, these will be replaced by actual protoc-generated code.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class PaginationRequest:
    """Request parameters for paginated list endpoints."""

    page: int = 1
    page_size: int = 20
    sort_by: str = ""
    sort_order: str = ""

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        return json.dumps(self.__dict__).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "PaginationRequest":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        return cls(**parsed)


@dataclass
class PaginationResponse:
    """Pagination metadata returned alongside list results."""

    total: int = 0
    page: int = 1
    page_size: int = 20
    pages: int = 0
    has_next: bool = False
    has_prev: bool = False

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        return json.dumps(self.__dict__).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "PaginationResponse":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        return cls(**parsed)


@dataclass
class ErrorResponse:
    """Structured error response for all API endpoints."""

    code: str = ""
    message: str = ""
    details: dict[str, str] = field(default_factory=dict)
    request_id: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "ErrorResponse":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "timestamp" in parsed and isinstance(parsed["timestamp"], str):
            parsed["timestamp"] = datetime.fromisoformat(parsed["timestamp"])
        return cls(**parsed)
