# aumos-proto

Canonical Protobuf schemas and compiled Python stubs for AumOS Enterprise platform events.

Every repo that publishes or consumes Kafka events imports from this package.

## Schema Structure

```
proto/aumos/
├── events/v1/          # Kafka event types
│   ├── agent_envelope.proto
│   ├── audit_event.proto
│   ├── model_lifecycle.proto
│   ├── governance_decision.proto
│   ├── security_alert.proto
│   └── usage_metrics.proto
├── models/v1/          # Shared domain model types
│   ├── tenant.proto
│   ├── model.proto
│   ├── agent.proto
│   └── job.proto
└── api/v1/             # Common API types
    ├── common.proto
    └── health.proto
```

## Installation

```bash
pip install aumos-proto
```

For development:

```bash
pip install -e ".[dev]"
```

## Usage Examples

### Publishing an agent event

```python
from aumos_proto.events.v1.agent_envelope_pb2 import AgentEnvelope

envelope = AgentEnvelope(
    tenant_id="tenant-abc",
    source_agent_id="orchestrator-1",
    target_agent_id="worker-2",
    message_type="task_request",
    privilege_level=3,
)
payload = envelope.SerializeToString()
```

### Consuming an audit event

```python
from aumos_proto.events.v1.audit_event_pb2 import AuditEvent

event = AuditEvent.FromString(raw_bytes)
print(f"Action: {event.action}, Outcome: {event.outcome}")
```

### Using model types

```python
from aumos_proto.models.v1.tenant_pb2 import Tenant, TenantStatus

tenant = Tenant(
    id="t-001",
    name="acme-corp",
    status=TenantStatus.ACTIVE,
)
```

## Development

### Generate stubs from proto files

```bash
make generate
```

### Run tests

```bash
make test
```

### Lint proto files and Python code

```bash
make lint
```

## Adding New Events

1. Add a new `.proto` file under `proto/aumos/events/v1/`
2. Follow the naming convention: `snake_case.proto`
3. Add a corresponding `_pb2.py` stub in `src/aumos_proto/events/v1/`
4. Export the new class from `src/aumos_proto/events/v1/__init__.py`
5. Add import tests to `tests/test_proto_imports.py`
6. Bump the package version in `pyproject.toml`

## Breaking Change Policy

Field numbering is **immutable** once published. Never:
- Remove existing fields (mark as `reserved` instead)
- Renumber fields
- Change field types

Always:
- Add new fields at the end with the next available number
- Start new enums with `UNSPECIFIED = 0`
- Bump the minor version for additive changes

## License

Apache 2.0 — Copyright 2026 AumOS Enterprise
