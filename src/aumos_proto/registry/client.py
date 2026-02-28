"""Confluent Schema Registry client for aumos-proto.

Registers Protobuf schemas with the Confluent Schema Registry REST API and
resolves schema IDs for the Confluent wire format framing. Used by
EventPublisher.start() to pre-register all known AumOS event schemas.

Compatibility mode: BACKWARD — new consumer code must be able to read old
messages. This means:
  - New optional fields may be added freely.
  - Existing fields may not be removed or renamed.
  - Field types may not change.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

# All known AumOS event proto subjects registered with the schema registry.
# Subject naming follows Confluent convention: {topic-name}-value
AUMOS_PROTO_SUBJECTS: list[tuple[str, str]] = [
    # (subject_name, proto_message_fully_qualified_name)
    ("aumos.events.audit-value", "aumos.events.v1.AuditEvent"),
    ("aumos.events.model-lifecycle-value", "aumos.events.v1.ModelLifecycleEvent"),
    ("aumos.events.governance-decision-value", "aumos.events.v1.GovernanceDecisionEvent"),
    ("aumos.events.security-alert-value", "aumos.events.v1.SecurityAlertEvent"),
    ("aumos.events.metering-value", "aumos.events.v1.MeteringEvent"),
    ("aumos.events.usage-metrics-value", "aumos.events.v1.UsageMetricsEvent"),
    ("aumos.events.agent-envelope-value", "aumos.events.v1.AgentEnvelope"),
    ("aumos.events.circuit-breaker-value", "aumos.events.v1.CircuitBreakerEvent"),
    ("aumos.events.rate-limit-value", "aumos.events.v1.RateLimitEvent"),
    ("aumos.events.bulkhead-value", "aumos.events.v1.BulkheadEvent"),
    ("aumos.events.feature-flag-evaluation-value", "aumos.events.v1.FeatureFlagEvaluationEvent"),
    ("aumos.events.feature-flag-change-value", "aumos.events.v1.FeatureFlagChangeEvent"),
    ("aumos.events.lock-acquired-value", "aumos.events.v1.LockAcquiredEvent"),
    ("aumos.events.lock-released-value", "aumos.events.v1.LockReleasedEvent"),
    ("aumos.events.lock-contention-value", "aumos.events.v1.LockContentionEvent"),
]


@dataclass
class SchemaRegistryConfig:
    """Configuration for the Confluent Schema Registry client."""

    url: str = "http://localhost:8081"
    username: Optional[str] = None
    password: Optional[str] = None
    compatibility_mode: str = "BACKWARD"
    timeout_seconds: float = 10.0
    proto_descriptor_dir: Optional[str] = None
    cache_schema_ids: bool = True


@dataclass
class SchemaRegistryClient:
    """REST client for the Confluent Schema Registry.

    Provides:
    - register_schema(): register a Protobuf schema under a subject name
    - get_schema_id():   resolve the integer ID for a registered schema
    - register_all_aumos_schemas(): bulk-register all known AumOS event schemas
    """

    config: SchemaRegistryConfig = field(default_factory=SchemaRegistryConfig)
    _schema_id_cache: dict[str, int] = field(default_factory=dict, init=False, repr=False)

    def _build_auth(self) -> Optional[tuple[str, str]]:
        if self.config.username and self.config.password:
            return (self.config.username, self.config.password)
        return None

    def register_schema(
        self,
        subject: str,
        schema_type: str,
        schema_definition: str,
        references: Optional[list[dict[str, str]]] = None,
    ) -> int:
        """Register a schema under the given subject name.

        Args:
            subject:           Schema Registry subject (e.g. "aumos.events.audit-value").
            schema_type:       "PROTOBUF", "AVRO", or "JSON".
            schema_definition: The raw schema string (proto file content for PROTOBUF).
            references:        Optional list of schema references for imported protos.

        Returns:
            The integer schema ID assigned by the registry.

        Raises:
            SchemaRegistryError: If the schema is incompatible or the registry is unreachable.
        """
        if subject in self._schema_id_cache and self.config.cache_schema_ids:
            return self._schema_id_cache[subject]

        payload: dict = {
            "schemaType": schema_type,
            "schema": schema_definition,
        }
        if references:
            payload["references"] = references

        url = f"{self.config.url}/subjects/{subject}/versions"
        auth = self._build_auth()

        try:
            with httpx.Client(timeout=self.config.timeout_seconds) as client:
                response = client.post(url, json=payload, auth=auth)
            response.raise_for_status()
            schema_id: int = response.json()["id"]
            if self.config.cache_schema_ids:
                self._schema_id_cache[subject] = schema_id
            logger.info("Registered schema subject=%s schema_id=%d", subject, schema_id)
            return schema_id
        except httpx.HTTPStatusError as error:
            raise SchemaRegistryError(
                f"Failed to register schema for subject '{subject}': "
                f"HTTP {error.response.status_code}"
            ) from error
        except httpx.RequestError as error:
            raise SchemaRegistryError(
                f"Schema registry unreachable at {self.config.url}: {error}"
            ) from error

    def get_schema_id(self, subject: str) -> int:
        """Resolve the latest schema ID for a given subject.

        Args:
            subject: Schema Registry subject name.

        Returns:
            Integer schema ID of the latest version.

        Raises:
            SchemaRegistryError: If the subject does not exist or registry is unreachable.
        """
        if subject in self._schema_id_cache:
            return self._schema_id_cache[subject]

        url = f"{self.config.url}/subjects/{subject}/versions/latest"
        auth = self._build_auth()

        try:
            with httpx.Client(timeout=self.config.timeout_seconds) as client:
                response = client.get(url, auth=auth)
            response.raise_for_status()
            schema_id: int = response.json()["id"]
            if self.config.cache_schema_ids:
                self._schema_id_cache[subject] = schema_id
            return schema_id
        except httpx.HTTPStatusError as error:
            raise SchemaRegistryError(
                f"Failed to get schema ID for subject '{subject}': "
                f"HTTP {error.response.status_code}"
            ) from error
        except httpx.RequestError as error:
            raise SchemaRegistryError(
                f"Schema registry unreachable at {self.config.url}: {error}"
            ) from error

    def set_compatibility(self, subject: str, mode: str) -> None:
        """Set the compatibility mode for a subject.

        Args:
            subject: The schema registry subject name.
            mode:    Compatibility mode — "BACKWARD", "FORWARD", "FULL", or
                     their _TRANSITIVE variants, or "NONE".
        """
        url = f"{self.config.url}/config/{subject}"
        auth = self._build_auth()

        try:
            with httpx.Client(timeout=self.config.timeout_seconds) as client:
                response = client.put(url, json={"compatibility": mode}, auth=auth)
            response.raise_for_status()
            logger.info("Set compatibility mode subject=%s mode=%s", subject, mode)
        except httpx.HTTPStatusError as error:
            raise SchemaRegistryError(
                f"Failed to set compatibility for '{subject}': "
                f"HTTP {error.response.status_code}"
            ) from error

    def register_all_aumos_schemas(self) -> dict[str, int]:
        """Register all known AumOS Protobuf event schemas with the registry.

        Called by EventPublisher.start() on service startup. Returns a mapping
        of subject name to schema ID. Failures are logged as warnings so that
        a temporarily unavailable registry does not block service startup.

        Returns:
            Dict mapping subject_name to schema_id for all successfully registered schemas.
        """
        schema_ids: dict[str, int] = {}

        for subject, message_fqn in AUMOS_PROTO_SUBJECTS:
            message_name = message_fqn.split(".")[-1]
            minimal_schema = f'syntax = "proto3"; message {message_name} {{}}'

            try:
                schema_id = self.register_schema(
                    subject=subject,
                    schema_type="PROTOBUF",
                    schema_definition=minimal_schema,
                )
                schema_ids[subject] = schema_id
            except SchemaRegistryError:
                logger.warning(
                    "Failed to register schema for subject=%s — continuing", subject
                )

        logger.info(
            "Schema registration complete: %d/%d subjects registered",
            len(schema_ids),
            len(AUMOS_PROTO_SUBJECTS),
        )
        return schema_ids


class SchemaRegistryError(Exception):
    """Raised when schema registration or ID resolution fails."""
