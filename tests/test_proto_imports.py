"""Verify all proto stubs can be imported."""


def test_import_agent_envelope() -> None:
    from aumos_proto.events.v1.agent_envelope_pb2 import AgentEnvelope
    envelope = AgentEnvelope(tenant_id="test-tenant", message_type="task_request")
    assert envelope.tenant_id == "test-tenant"


def test_import_audit_event() -> None:
    from aumos_proto.events.v1.audit_event_pb2 import AuditEvent
    event = AuditEvent(tenant_id="test-tenant", action="create")
    assert event.action == "create"


def test_import_model_lifecycle() -> None:
    from aumos_proto.events.v1.model_lifecycle_pb2 import ModelLifecycleEvent
    event = ModelLifecycleEvent(model_id="model-1")
    assert event.model_id == "model-1"


def test_import_governance_decision() -> None:
    from aumos_proto.events.v1.governance_decision_pb2 import GovernanceDecisionEvent
    event = GovernanceDecisionEvent(policy_id="policy-1")
    assert event.policy_id == "policy-1"


def test_import_security_alert() -> None:
    from aumos_proto.events.v1.security_alert_pb2 import SecurityAlertEvent
    event = SecurityAlertEvent(alert_type="injection_attempt")
    assert event.alert_type == "injection_attempt"


def test_import_usage_metrics() -> None:
    from aumos_proto.events.v1.usage_metrics_pb2 import UsageMetricsEvent
    event = UsageMetricsEvent(metric_type="api_call", value=1.0)
    assert event.value == 1.0


def test_import_tenant() -> None:
    from aumos_proto.models.v1.tenant_pb2 import Tenant
    tenant = Tenant(id="t-1", name="test")
    assert tenant.name == "test"


def test_import_model() -> None:
    from aumos_proto.models.v1.model_pb2 import Model
    model = Model(id="m-1", name="test-model")
    assert model.name == "test-model"


def test_import_agent() -> None:
    from aumos_proto.models.v1.agent_pb2 import Agent
    agent = Agent(id="a-1", privilege_level=3)
    assert agent.privilege_level == 3


def test_import_job() -> None:
    from aumos_proto.models.v1.job_pb2 import Job
    job = Job(id="j-1", job_type="synthesis")
    assert job.job_type == "synthesis"


def test_import_common() -> None:
    from aumos_proto.api.v1.common_pb2 import ErrorResponse, PaginationRequest
    req = PaginationRequest(page=1, page_size=20)
    assert req.page_size == 20


def test_import_health() -> None:
    from aumos_proto.api.v1.health_pb2 import HealthResponse
    resp = HealthResponse(service="test", status="healthy")
    assert resp.status == "healthy"


def test_serialization_roundtrip() -> None:
    from aumos_proto.events.v1.agent_envelope_pb2 import AgentEnvelope
    original = AgentEnvelope(
        tenant_id="tenant-1",
        message_type="task_request",
        privilege_level=3,
    )
    serialized = original.SerializeToString()
    deserialized = AgentEnvelope.FromString(serialized)
    assert deserialized.tenant_id == "tenant-1"
    assert deserialized.privilege_level == 3
