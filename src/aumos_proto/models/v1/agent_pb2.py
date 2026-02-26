"""Generated-compatible Python stubs for agent.proto.

These are Python dataclass implementations mirroring the Protobuf definitions.
In production, these will be replaced by actual protoc-generated code.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum


class AgentType(IntEnum):
    """Enum for agent autonomy type."""

    AGENT_TYPE_UNSPECIFIED = 0
    AUTONOMOUS = 1
    SEMI_AUTONOMOUS = 2
    SUPERVISED = 3
    TOOL = 4


class AgentStatus(IntEnum):
    """Enum for agent runtime status."""

    AGENT_STATUS_UNSPECIFIED = 0
    IDLE = 1
    RUNNING = 2
    PAUSED = 3
    ERROR = 4
    TERMINATED = 5


@dataclass
class Agent:
    """Agent represents an autonomous or semi-autonomous AI agent in AumOS."""

    id: str = ""
    tenant_id: str = ""
    name: str = ""
    description: str = ""
    agent_type: AgentType = AgentType.AGENT_TYPE_UNSPECIFIED
    privilege_level: int = 0
    status: AgentStatus = AgentStatus.AGENT_STATUS_UNSPECIFIED
    capabilities: list[str] = field(default_factory=list)
    owner_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def SerializeToString(self) -> bytes:
        """Compatibility method for Protobuf serialization."""
        data = {
            k: (
                v.isoformat() if isinstance(v, datetime)
                else int(v) if isinstance(v, (AgentType, AgentStatus))
                else v
            )
            for k, v in self.__dict__.items()
        }
        return json.dumps(data).encode("utf-8")

    @classmethod
    def FromString(cls, data: bytes) -> "Agent":
        """Compatibility method for Protobuf deserialization."""
        parsed = json.loads(data.decode("utf-8"))
        if "created_at" in parsed and isinstance(parsed["created_at"], str):
            parsed["created_at"] = datetime.fromisoformat(parsed["created_at"])
        if "agent_type" in parsed and isinstance(parsed["agent_type"], int):
            parsed["agent_type"] = AgentType(parsed["agent_type"])
        if "status" in parsed and isinstance(parsed["status"], int):
            parsed["status"] = AgentStatus(parsed["status"])
        return cls(**parsed)
