"""Tests for the Confluent Schema Registry integration (Gap 537).

Tests cover:
- Wire format framing (encode/decode)
- SchemaRegistryClient (mocked HTTP calls)
- AUMOS_PROTO_SUBJECTS completeness
"""
from __future__ import annotations

import struct
import pytest


# ---------------------------------------------------------------------------
# Framing utilities (no network required)
# ---------------------------------------------------------------------------


def test_encode_with_schema_id_produces_5_byte_header() -> None:
    from aumos_proto.registry.framing import MAGIC_BYTE, encode_with_schema_id

    payload = b"test-payload"
    schema_id = 42
    framed = encode_with_schema_id(schema_id, payload)

    assert len(framed) == 5 + len(payload)
    assert framed[0] == MAGIC_BYTE
    extracted_id = struct.unpack_from(">I", framed, 1)[0]
    assert extracted_id == schema_id
    assert framed[5:] == payload


def test_decode_schema_id_extracts_correct_id() -> None:
    from aumos_proto.registry.framing import decode_schema_id, encode_with_schema_id

    schema_id = 12345
    payload = b"proto-bytes"
    framed = encode_with_schema_id(schema_id, payload)

    assert decode_schema_id(framed) == schema_id


def test_strip_schema_framing_returns_id_and_payload() -> None:
    from aumos_proto.registry.framing import encode_with_schema_id, strip_schema_framing

    schema_id = 99
    payload = b"serialized-event"
    framed = encode_with_schema_id(schema_id, payload)

    extracted_id, extracted_payload = strip_schema_framing(framed)
    assert extracted_id == schema_id
    assert extracted_payload == payload


def test_decode_schema_id_raises_on_wrong_magic_byte() -> None:
    from aumos_proto.registry.framing import decode_schema_id

    bad_framing = b"\x01\x00\x00\x00\x2a" + b"payload"
    with pytest.raises(ValueError, match="magic byte"):
        decode_schema_id(bad_framing)


def test_decode_schema_id_raises_on_too_short_message() -> None:
    from aumos_proto.registry.framing import decode_schema_id

    with pytest.raises(ValueError, match="too short"):
        decode_schema_id(b"\x00\x00")


def test_encode_decode_roundtrip_for_large_schema_id() -> None:
    from aumos_proto.registry.framing import encode_with_schema_id, strip_schema_framing

    schema_id = 2**31 - 1  # max value for 4-byte unsigned
    payload = b"\x0a\x05hello"
    framed = encode_with_schema_id(schema_id, payload)
    extracted_id, extracted_payload = strip_schema_framing(framed)

    assert extracted_id == schema_id
    assert extracted_payload == payload


# ---------------------------------------------------------------------------
# SchemaRegistryConfig defaults
# ---------------------------------------------------------------------------


def test_schema_registry_config_defaults() -> None:
    from aumos_proto.registry.client import SchemaRegistryConfig

    config = SchemaRegistryConfig()
    assert config.url == "http://localhost:8081"
    assert config.compatibility_mode == "BACKWARD"
    assert config.cache_schema_ids is True
    assert config.username is None


# ---------------------------------------------------------------------------
# AUMOS_PROTO_SUBJECTS completeness
# ---------------------------------------------------------------------------


def test_all_aumos_subjects_have_unique_names() -> None:
    from aumos_proto.registry.client import AUMOS_PROTO_SUBJECTS

    subject_names = [s for s, _ in AUMOS_PROTO_SUBJECTS]
    assert len(subject_names) == len(set(subject_names)), "Duplicate subject names found"


def test_resilience_events_in_subjects() -> None:
    from aumos_proto.registry.client import AUMOS_PROTO_SUBJECTS

    subject_names = {s for s, _ in AUMOS_PROTO_SUBJECTS}
    assert "aumos.events.circuit-breaker-value" in subject_names
    assert "aumos.events.rate-limit-value" in subject_names
    assert "aumos.events.bulkhead-value" in subject_names


def test_feature_flag_events_in_subjects() -> None:
    from aumos_proto.registry.client import AUMOS_PROTO_SUBJECTS

    subject_names = {s for s, _ in AUMOS_PROTO_SUBJECTS}
    assert "aumos.events.feature-flag-evaluation-value" in subject_names
    assert "aumos.events.feature-flag-change-value" in subject_names


def test_lock_events_in_subjects() -> None:
    from aumos_proto.registry.client import AUMOS_PROTO_SUBJECTS

    subject_names = {s for s, _ in AUMOS_PROTO_SUBJECTS}
    assert "aumos.events.lock-acquired-value" in subject_names
    assert "aumos.events.lock-released-value" in subject_names
    assert "aumos.events.lock-contention-value" in subject_names


def test_core_events_in_subjects() -> None:
    from aumos_proto.registry.client import AUMOS_PROTO_SUBJECTS

    subject_names = {s for s, _ in AUMOS_PROTO_SUBJECTS}
    assert "aumos.events.audit-value" in subject_names
    assert "aumos.events.model-lifecycle-value" in subject_names
    assert "aumos.events.governance-decision-value" in subject_names
    assert "aumos.events.security-alert-value" in subject_names


# ---------------------------------------------------------------------------
# SchemaRegistryClient (mocked HTTP)
# ---------------------------------------------------------------------------


def test_schema_registry_client_caches_schema_id_after_register() -> None:
    """Verify that a second call with the same subject returns from cache."""
    from aumos_proto.registry.client import SchemaRegistryClient, SchemaRegistryConfig

    client = SchemaRegistryClient(config=SchemaRegistryConfig())
    # Manually seed the cache to avoid real HTTP call
    client._schema_id_cache["aumos.events.audit-value"] = 7

    result = client.register_schema(
        subject="aumos.events.audit-value",
        schema_type="PROTOBUF",
        schema_definition='syntax = "proto3"; message AuditEvent {}',
    )
    assert result == 7  # returned from cache without HTTP call


def test_schema_registry_client_get_schema_id_returns_from_cache() -> None:
    from aumos_proto.registry.client import SchemaRegistryClient, SchemaRegistryConfig

    client = SchemaRegistryClient(config=SchemaRegistryConfig())
    client._schema_id_cache["aumos.events.metering-value"] = 42

    result = client.get_schema_id("aumos.events.metering-value")
    assert result == 42
