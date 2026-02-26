"""AumOS shared model type stubs — v1."""

from aumos_proto.models.v1.agent_pb2 import Agent, AgentStatus, AgentType
from aumos_proto.models.v1.job_pb2 import Job, JobStatus
from aumos_proto.models.v1.model_pb2 import Model, ModelStatus
from aumos_proto.models.v1.tenant_pb2 import Tenant, TenantQuota, TenantStatus

__all__ = [
    "Agent",
    "AgentStatus",
    "AgentType",
    "Job",
    "JobStatus",
    "Model",
    "ModelStatus",
    "Tenant",
    "TenantQuota",
    "TenantStatus",
]
