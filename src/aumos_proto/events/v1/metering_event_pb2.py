"""Generated-compatible Python stubs for metering_event.proto.

These are Python dataclass implementations mirroring the Protobuf definitions.
In production, these will be replaced by actual protoc-generated code.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TokenUsage:
    """Token consumption details for an LLM call."""

    model_id: str = ""
    provider: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        return json.dumps(self.__dict__).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "TokenUsage":
        """Compatibility method for Protobuf deserialization."""
        return cls(**json.loads(data.decode("utf-8")))


@dataclass
class InferenceUsage:
    """Compute resource usage for a model inference call."""

    model_id: str = ""
    latency_ms: float = 0.0
    compute_ms: int = 0
    hardware_tier: str = ""

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        return json.dumps(self.__dict__).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "InferenceUsage":
        """Compatibility method for Protobuf deserialization."""
        return cls(**json.loads(data.decode("utf-8")))


@dataclass
class StorageUsage:
    """Storage I/O usage for a single operation."""

    bytes_read: int = 0
    bytes_written: int = 0
    storage_tier: str = ""

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        return json.dumps(self.__dict__).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "StorageUsage":
        """Compatibility method for Protobuf deserialization."""
        return cls(**json.loads(data.decode("utf-8")))


@dataclass
class SyntheticDataUsage:
    """Resource usage for a synthetic data generation operation."""

    records_generated: int = 0
    data_modality: str = ""
    generation_duration_ms: float = 0.0

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        return json.dumps(self.__dict__).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "SyntheticDataUsage":
        """Compatibility method for Protobuf deserialization."""
        return cls(**json.loads(data.decode("utf-8")))


@dataclass
class MeteringEvent:
    """A single metering event recording resource consumption for a tenant.

    Exactly one of token_usage, inference_usage, storage_usage, or synthetic_usage
    should be set (mirrors the protobuf oneof resource field).
    """

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    project_id: str = ""
    team_id: str = ""
    service_name: str = ""
    operation: str = ""
    timestamp_ms: int = 0
    token_usage: Optional[TokenUsage] = None
    inference_usage: Optional[InferenceUsage] = None
    storage_usage: Optional[StorageUsage] = None
    synthetic_usage: Optional[SyntheticDataUsage] = None
    labels: dict[str, str] = field(default_factory=dict)

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data: dict = {
            "event_id": self.event_id,
            "tenant_id": self.tenant_id,
            "project_id": self.project_id,
            "team_id": self.team_id,
            "service_name": self.service_name,
            "operation": self.operation,
            "timestamp_ms": self.timestamp_ms,
            "labels": self.labels,
        }
        if self.token_usage is not None:
            data["token_usage"] = self.token_usage.__dict__
        if self.inference_usage is not None:
            data["inference_usage"] = self.inference_usage.__dict__
        if self.storage_usage is not None:
            data["storage_usage"] = self.storage_usage.__dict__
        if self.synthetic_usage is not None:
            data["synthetic_usage"] = self.synthetic_usage.__dict__
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "MeteringEvent":
        """Compatibility method for Protobuf deserialization.

        Only the known schema fields are extracted from the parsed payload.
        Unknown keys are silently ignored to prevent arbitrary field injection
        via crafted byte payloads.
        """
        parsed: dict = json.loads(data.decode("utf-8"))

        token_usage: Optional[TokenUsage] = None
        inference_usage: Optional[InferenceUsage] = None
        storage_usage: Optional[StorageUsage] = None
        synthetic_usage: Optional[SyntheticDataUsage] = None

        if "token_usage" in parsed:
            token_usage = TokenUsage(**parsed["token_usage"])
        if "inference_usage" in parsed:
            inference_usage = InferenceUsage(**parsed["inference_usage"])
        if "storage_usage" in parsed:
            storage_usage = StorageUsage(**parsed["storage_usage"])
        if "synthetic_usage" in parsed:
            synthetic_usage = SyntheticDataUsage(**parsed["synthetic_usage"])

        # Explicitly name every known field — no splat to prevent injection.
        return cls(
            event_id=parsed.get("event_id", ""),
            tenant_id=parsed.get("tenant_id", ""),
            project_id=parsed.get("project_id", ""),
            team_id=parsed.get("team_id", ""),
            service_name=parsed.get("service_name", ""),
            operation=parsed.get("operation", ""),
            timestamp_ms=parsed.get("timestamp_ms", 0),
            labels=parsed.get("labels", {}),
            token_usage=token_usage,
            inference_usage=inference_usage,
            storage_usage=storage_usage,
            synthetic_usage=synthetic_usage,
        )
