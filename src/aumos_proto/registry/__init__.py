"""Schema registry integration for aumos-proto.

Provides SchemaRegistryClient for registering Protobuf schemas with
Confluent Schema Registry and resolving schema IDs at publish time.

Wire format: magic byte (0x00) + 4-byte big-endian schema ID + payload bytes.
This is the standard Confluent Schema Registry framing used by all Confluent clients.
"""
from aumos_proto.registry.client import SchemaRegistryClient, SchemaRegistryConfig
from aumos_proto.registry.framing import (
    MAGIC_BYTE,
    decode_schema_id,
    encode_with_schema_id,
    strip_schema_framing,
)

__all__ = [
    "MAGIC_BYTE",
    "SchemaRegistryClient",
    "SchemaRegistryConfig",
    "decode_schema_id",
    "encode_with_schema_id",
    "strip_schema_framing",
]
