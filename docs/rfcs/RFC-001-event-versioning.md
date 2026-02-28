# RFC-001: AumOS Event Versioning Strategy

**Status:** Accepted
**Date:** 2026-02-28
**Author:** AumOS Platform Team
**Repo:** aumos-proto

---

## Problem

AumOS cross-service events (Kafka messages) evolve over time. A `ModelLifecycleEvent`
that gains a `training_config` field in v1.1 must be handled gracefully by consumers
still running v1.0 code. Without a documented strategy, each team invents its own
approach — some embed a `version` field in the payload, some use topic-name versioning
(`aumos.models.lifecycle.v2`), some rely on the schema registry version. Inconsistency
causes production incidents when consumers receive messages they cannot parse.

---

## Decision

### 1. Schema Registry Is the Source of Schema Truth

Schema versioning is managed by the **Confluent Schema Registry**, not by fields in
the event payload. The schema registry assigns an integer **schema ID** to every
registered schema version. Consumers resolve the schema from the schema ID embedded
in the Confluent wire format header — they do not parse a `version` string from the payload.

**Implication:** The `version: str = Field(default="v1")` field in `BaseEvent` is
**deprecated**. It may be read by legacy consumers but must not be used to determine
how to deserialize the event. The schema ID in the 5-byte Confluent framing header is
the authoritative version indicator.

### 2. Topic Naming Convention

Topics use the pattern: `aumos.{domain}.{event_type}`

Examples:
- `aumos.models.lifecycle`
- `aumos.governance.decision`
- `aumos.security.alert`
- `aumos.metering.usage`
- `aumos.agents.envelope`

**No version in the topic name.** Version is tracked in the schema registry, not the
topic name. Topic names are permanent — creating `aumos.models.lifecycle.v2` would
require migrating all consumers and producers simultaneously, which is operationally
expensive and error-prone.

### 3. Compatibility Mode: BACKWARD

All schemas are registered with **BACKWARD** compatibility. This means:

- A new schema version must be readable by consumers using the **previous** schema version.
- Consumers are always upgraded **before** producers.
- Upgrade order: consumers first, producers second.

BACKWARD compatibility allows:
- Adding new optional fields (they default to zero-value for old consumers).
- Adding new enum values (old consumers receive UNSPECIFIED or the numeric value).

BACKWARD compatibility prohibits:
- Removing fields (old consumers will have zero-value gaps).
- Renumbering fields (corrupts data for consumers using the old schema).
- Changing field types (causes deserialization failures).
- Removing enum values (old messages become undecodable).

### 4. Non-Breaking Schema Evolution (MINOR Changes)

For backwards-compatible additions:

1. Add the new field at the next available field number in the `.proto` file.
2. Run `buf generate` to regenerate stubs.
3. Open a PR — `buf breaking` CI gate verifies the change is non-breaking.
4. After merge, the schema registry auto-registers the new version on the next
   `EventPublisher.start()` call.

### 5. Breaking Schema Evolution (MAJOR Changes)

If a breaking change is unavoidable (field removal, type change):

1. Create a **new proto message** with a different name (e.g., `ModelLifecycleEventV2`).
2. Create a **new topic** (e.g., `aumos.models.lifecycle.v2`) for the new message.
3. Deploy producers to publish to **both** the old and new topics simultaneously.
4. Migrate consumers to the new topic over a **minimum 6-month parallel period**.
5. After all consumers are migrated, deprecate the old topic and stop publishing to it.
6. After an additional 30-day grace period, decommission the old topic.

The old proto message and topic are never deleted — they are marked as deprecated in
the proto file using a `reserved` statement and a comment.

### 6. Reserved Field Policy

When a field is deprecated or removed from a message, it **must** be marked as reserved
to prevent future reuse of the field number:

```proto
message ModelLifecycleEvent {
  reserved 5;              // field 5 was "version" — deprecated 2026-Q1
  reserved "version";      // field name reserved to prevent typo reuse

  string event_id = 1;
  // ... remaining fields
}
```

Never delete a reserved statement once published. Field numbers 1-15 are single-byte
tags on the wire — prefer these for the highest-frequency fields.

### 7. Schema Registry Subject Naming

Schema Registry subjects follow the Confluent convention:

- Value schemas: `{topic-name}-value`
- Key schemas: `{topic-name}-key` (if key is schema-registered; AumOS uses string keys)

Examples:
- `aumos.models.lifecycle-value`
- `aumos.governance.decision-value`

### 8. Consumer Upgrade Order

**Rule:** Always upgrade consumers before producers when deploying a schema change.

Rationale: BACKWARD compatibility guarantees that a new schema can be read by old
consumers. The reverse (FORWARD) is not guaranteed. Therefore:

1. Deploy consumers with the new schema version (they can still read old messages).
2. Wait for all consumer instances to be running the new version.
3. Deploy producers with the new schema version (they now emit new-format messages).

Kafka's consumer group offset tracking ensures no messages are missed during the upgrade.

---

## Consequences

**Positive:**
- Schema evolution is safe and auditable — the schema registry tracks every version.
- No need to parse a `version` field — the wire format header carries the schema ID.
- Breaking changes are caught at PR time by `buf breaking` CI gate.
- Topic names are stable across schema versions.

**Negative:**
- The `version` field in `BaseEvent` must be deprecated gracefully — existing services
  that write or read it need to be updated.
- Schema registry becomes a dependency for event publishing — `EventPublisher.start()`
  will fail fast if the registry is unreachable (this is intentional: publishing with
  an unregistered schema corrupts consumers).

---

## Implementation References

- Schema registry client: `src/aumos_proto/registry/client.py`
- Wire format framing: `src/aumos_proto/registry/framing.py`
- buf breaking CI gate: `.github/workflows/proto-check.yml`
- Breaking rules config: `buf.yaml` (FILE-level breaking rules)
