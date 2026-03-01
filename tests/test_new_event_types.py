"""Tests for the 3 new proto event types added in Gap 534.

Covers: resilience_event, feature_flag_event, lock_event
"""
from __future__ import annotations


def test_circuit_breaker_event_import_and_defaults() -> None:
    from aumos_proto.events.v1.resilience_event_pb2 import CircuitBreakerEvent

    event = CircuitBreakerEvent(
        circuit_name="payment-service",
        from_state="closed",
        to_state="open",
        source_service="aumos-gateway",
        failure_count=5,
    )
    assert event.circuit_name == "payment-service"
    assert event.from_state == "closed"
    assert event.to_state == "open"
    assert event.failure_count == 5
    assert event.tenant_id == ""
    assert event.event_id != ""


def test_rate_limit_event_import_and_defaults() -> None:
    from aumos_proto.events.v1.resilience_event_pb2 import RateLimitEvent

    event = RateLimitEvent(
        tenant_id="tenant-abc",
        path="/api/v1/models/deploy",
        limit=100,
        current_count=101,
        rejected=True,
        source_service="aumos-api-gateway",
    )
    assert event.path == "/api/v1/models/deploy"
    assert event.rejected is True
    assert event.limit == 100


def test_bulkhead_event_import_and_defaults() -> None:
    from aumos_proto.events.v1.resilience_event_pb2 import BulkheadEvent

    event = BulkheadEvent(
        bulkhead_name="inference-pool",
        max_concurrent_calls=10,
        active_calls=10,
        rejected=True,
    )
    assert event.rejected is True
    assert event.active_calls == 10


def test_resilience_event_serialization_roundtrip() -> None:
    from aumos_proto.events.v1.resilience_event_pb2 import CircuitBreakerEvent

    original = CircuitBreakerEvent(
        tenant_id="t-1",
        circuit_name="model-registry",
        from_state="half_open",
        to_state="closed",
        source_service="aumos-mlops",
        failure_count=0,
        success_count=3,
    )
    serialized = original.SerializeToString()
    restored = CircuitBreakerEvent.FromString(serialized)

    assert restored.tenant_id == original.tenant_id
    assert restored.circuit_name == original.circuit_name
    assert restored.from_state == original.from_state
    assert restored.to_state == original.to_state
    assert restored.failure_count == 0
    assert restored.success_count == 3


def test_feature_flag_evaluation_event() -> None:
    from aumos_proto.events.v1.feature_flag_event_pb2 import FeatureFlagEvaluationEvent

    event = FeatureFlagEvaluationEvent(
        tenant_id="tenant-xyz",
        flag_key="enable_llm_v2_routing",
        enabled=True,
        evaluated_for="user-123",
        source_service="aumos-llm-serving",
    )
    assert event.flag_key == "enable_llm_v2_routing"
    assert event.enabled is True
    assert event.evaluated_for == "user-123"


def test_feature_flag_change_event() -> None:
    from aumos_proto.events.v1.feature_flag_event_pb2 import FeatureFlagChangeEvent

    event = FeatureFlagChangeEvent(
        tenant_id="tenant-xyz",
        flag_key="synthetic_data_v2",
        previous_enabled=False,
        new_enabled=True,
        changed_by="admin@muveraai.com",
        change_reason="Rollout to 100% of tenants after successful canary.",
    )
    assert event.previous_enabled is False
    assert event.new_enabled is True


def test_feature_flag_serialization_roundtrip() -> None:
    from aumos_proto.events.v1.feature_flag_event_pb2 import FeatureFlagEvaluationEvent

    original = FeatureFlagEvaluationEvent(
        tenant_id="t-99",
        flag_key="enable_zkp_compliance",
        enabled=False,
        evaluated_for="team-ops",
        source_service="aumos-governance",
        context={"region": "us-east-1", "tier": "enterprise"},
    )
    serialized = original.SerializeToString()
    restored = FeatureFlagEvaluationEvent.FromString(serialized)

    assert restored.flag_key == "enable_zkp_compliance"
    assert restored.enabled is False
    assert restored.context == {"region": "us-east-1", "tier": "enterprise"}


def test_lock_acquired_event() -> None:
    from aumos_proto.events.v1.lock_event_pb2 import LockAcquiredEvent

    event = LockAcquiredEvent(
        tenant_id="tenant-abc",
        lock_name="model-deploy-mutex",
        lock_owner="aumos-mlops-pod-7d9f8",
        ttl_seconds=30,
        source_service="aumos-mlops",
    )
    assert event.lock_name == "model-deploy-mutex"
    assert event.ttl_seconds == 30
    assert event.lock_owner == "aumos-mlops-pod-7d9f8"


def test_lock_released_event() -> None:
    from aumos_proto.events.v1.lock_event_pb2 import LockReleasedEvent

    event = LockReleasedEvent(
        tenant_id="tenant-abc",
        lock_name="model-deploy-mutex",
        lock_owner="aumos-mlops-pod-7d9f8",
        timed_out=False,
    )
    assert event.timed_out is False


def test_lock_contention_event() -> None:
    from aumos_proto.events.v1.lock_event_pb2 import LockContentionEvent

    event = LockContentionEvent(
        tenant_id="tenant-abc",
        lock_name="data-export-lock",
        requesting_owner="aumos-export-pod-2",
        current_owner="aumos-export-pod-1",
        wait_seconds=5,
    )
    assert event.wait_seconds == 5
    assert event.requesting_owner == "aumos-export-pod-2"


def test_lock_event_serialization_roundtrip() -> None:
    from aumos_proto.events.v1.lock_event_pb2 import LockAcquiredEvent

    original = LockAcquiredEvent(
        tenant_id="t-1",
        lock_name="approval-workflow-lock",
        lock_owner="aumos-approval-pod-3",
        ttl_seconds=60,
        source_service="aumos-approval-workflow",
    )
    serialized = original.SerializeToString()
    restored = LockAcquiredEvent.FromString(serialized)

    assert restored.lock_name == original.lock_name
    assert restored.lock_owner == original.lock_owner
    assert restored.ttl_seconds == 60


def test_events_v1_init_exports_new_types() -> None:
    """Verify the v1 __init__.py exports all new event types."""
    from aumos_proto.events import v1

    assert hasattr(v1, "CircuitBreakerEvent")
    assert hasattr(v1, "RateLimitEvent")
    assert hasattr(v1, "BulkheadEvent")
    assert hasattr(v1, "FeatureFlagEvaluationEvent")
    assert hasattr(v1, "FeatureFlagChangeEvent")
    assert hasattr(v1, "LockAcquiredEvent")
    assert hasattr(v1, "LockReleasedEvent")
    assert hasattr(v1, "LockContentionEvent")
