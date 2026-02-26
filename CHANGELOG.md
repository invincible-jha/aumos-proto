# Changelog

All notable changes to `aumos-proto` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-02-26

### Added
- Initial Protobuf schemas for all AumOS event types:
  - `AgentEnvelope` — standard envelope for agent-to-agent messages
  - `AuditEvent` — user and system action audit trail
  - `ModelLifecycleEvent` — ML model state transitions
  - `GovernanceDecisionEvent` — policy evaluation outcomes
  - `SecurityAlertEvent` — threat detection and security alerts
  - `UsageMetricsEvent` — resource usage for billing and monitoring
- Shared model type schemas:
  - `Tenant` — organizational unit with quota management
  - `Model` — ML model artifact tracking
  - `Agent` — autonomous agent definitions
  - `Job` — async task execution records
- Common API type schemas:
  - `PaginationRequest` / `PaginationResponse`
  - `ErrorResponse`
  - `HealthResponse` / `ComponentHealth`
- Python dataclass stubs mirroring all Protobuf definitions
- buf configuration for schema linting and breaking change detection
- Import tests for all message types and serialization roundtrip
