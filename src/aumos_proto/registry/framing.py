"""Confluent Schema Registry wire format framing utilities.

The Confluent Schema Registry wire format prefixes every serialized message with
a 5-byte header:
    byte 0:     magic byte = 0x00 (identifies schema registry framing)
    bytes 1-4:  schema ID as 4-byte big-endian unsigned integer

This module provides encode/decode helpers that are wire-format correct
regardless of which serializer (betterproto, standard protoc, or JSON) is used.
"""
from __future__ import annotations

import struct

MAGIC_BYTE: int = 0x00
_HEADER_FORMAT: str = ">bI"  # big-endian: 1 signed byte + 4-byte unsigned int
_HEADER_SIZE: int = 5


def encode_with_schema_id(schema_id: int, payload: bytes) -> bytes:
    """Prepend the 5-byte Confluent framing header to a serialized payload.

    Args:
        schema_id: The integer schema ID returned by the schema registry
                   after registering the schema.
        payload:   The serialized Protobuf bytes (from SerializeToString() or
                   the betterproto equivalent).

    Returns:
        Framed bytes ready for publication to Kafka.
    """
    header = struct.pack(_HEADER_FORMAT, MAGIC_BYTE, schema_id)
    return header + payload


def decode_schema_id(framed: bytes) -> int:
    """Extract the schema ID from a Confluent-framed message.

    Args:
        framed: Raw bytes from a Kafka consumer record.

    Returns:
        The integer schema ID embedded in the 5-byte header.

    Raises:
        ValueError: If the magic byte is missing (message is not schema-registry framed).
    """
    if len(framed) < _HEADER_SIZE:
        raise ValueError(
            f"Message is too short to be schema-registry framed: {len(framed)} bytes"
        )
    magic, schema_id = struct.unpack_from(_HEADER_FORMAT, framed, 0)
    if magic != MAGIC_BYTE:
        raise ValueError(
            f"Expected Confluent magic byte 0x00, got 0x{magic:02x}. "
            "This message may not be schema-registry framed."
        )
    return int(schema_id)


def strip_schema_framing(framed: bytes) -> tuple[int, bytes]:
    """Split a framed message into its schema ID and payload.

    Args:
        framed: Raw bytes from a Kafka consumer record.

    Returns:
        A tuple of (schema_id, payload_bytes) where payload_bytes is the
        Protobuf-serialized message without the framing header.

    Raises:
        ValueError: If the magic byte is incorrect.
    """
    schema_id = decode_schema_id(framed)
    payload = framed[_HEADER_SIZE:]
    return schema_id, payload
