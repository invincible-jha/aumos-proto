# CLAUDE.md — AumOS Proto

## Project Context
`aumos-proto` contains the canonical Protobuf schemas for all AumOS Enterprise event types and shared model definitions. Every repo that publishes or consumes Kafka events imports compiled stubs from this package.

## What This Package Provides
- Protobuf .proto schemas for events, models, and API types
- Pre-compiled Python stubs (dataclass-based for development, protoc-generated for production)
- buf configuration for linting and breaking change detection

## Tech Stack
- Protobuf 3, buf for schema management
- Python 3.11+, dataclasses for stub implementations

## Coding Standards
- All proto files use proto3 syntax
- Package naming: aumos.{category}.v1
- Field numbering is IMMUTABLE once published
- NEVER remove or renumber fields — mark as reserved
- New fields are always ADDED at the end with next available number
- Enums always start with UNSPECIFIED = 0

## Architecture
This is a LIBRARY, not a service. No main.py, no Dockerfile.
Consumed by: aumos-common (events module), all 75 AumOS repos.
