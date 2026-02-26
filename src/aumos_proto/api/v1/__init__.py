"""AumOS API type stubs — v1."""

from aumos_proto.api.v1.common_pb2 import ErrorResponse, PaginationRequest, PaginationResponse
from aumos_proto.api.v1.health_pb2 import ComponentHealth, HealthResponse

__all__ = [
    "ErrorResponse",
    "PaginationRequest",
    "PaginationResponse",
    "ComponentHealth",
    "HealthResponse",
]
