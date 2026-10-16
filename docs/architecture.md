# InfraPulse — System Architecture

**Version:** 0.1  
**Status:** Proposed  
**Last updated:** October 2026

## 1. Overview

InfraPulse is a monitoring application designed to collect,
store, and retrieve infrastructure metrics.

The initial version uses synthetic data to simulate readings
from infrastructure devices.

The application will provide APIs for device registration,
metric ingestion, and historical data retrieval.

The primary objective of v1 is to establish a working
end-to-end data flow with a maintainable backend structure.

## 2. Architecture Style

The initial implementation follows a modular monolith approach.

A single FastAPI application will handle:

- Device registration and management
- Metric ingestion and validation
- Metric retrieval
- Device status queries

Application modules will have separate responsibilities
while sharing the same deployment and database.

A standalone Python simulator will generate synthetic
metric readings and submit them through the ingestion API.

### Rationale

A modular monolith is sufficient for the initial scope.

It avoids the operational overhead of managing multiple
services while allowing application responsibilities to
remain separated.

Service decomposition may be reconsidered if independent
scaling, deployment, or ownership becomes necessary.

## 3. System Components

| Component | Responsibility | Technology |
|-----------|----------------|------------|
| Simulator | Generate synthetic device readings | Python |
| API | Validate requests and expose application operations | FastAPI |
| Device module | Manage registered devices | Python |
| Metrics module | Ingest and retrieve readings | Python |
| Persistence | Store devices and historical metrics | PostgreSQL |
| API consumer | Query monitoring information | HTTP client |

The dashboard is planned but is not part of the initial
backend implementation.

## 4. Data Flow

### Metric Ingestion

1. A device is registered through the API.
2. The simulator generates readings for that device.
3. Readings are submitted to the ingestion endpoint.
4. FastAPI validates the request.
5. The metrics module stores the readings in PostgreSQL.
6. The API returns the ingestion result.

### Metric Retrieval

1. A client requests metrics for a registered device.
2. The API validates the device identifier and query parameters.
3. The metrics module queries PostgreSQL.
4. The API returns the requested readings.

Historical queries will support time-range filtering.

## 5. Initial Data Model

### devices

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | Primary key |
| name | VARCHAR(100) | Device name |
| device_type | VARCHAR(50) | Server, sensor, etc. |
| location | VARCHAR(100) | Logical location |
| created_at | TIMESTAMPTZ | Registration timestamp |

### metric_readings

| Column | Type | Notes |
|--------|------|-------|
| id | BIGINT | Primary key |
| device_id | UUID | References devices.id |
| metric_name | VARCHAR(50) | CPU, memory, temperature |
| metric_value | DOUBLE PRECISION | Numeric reading |
| recorded_at | TIMESTAMPTZ | Measurement timestamp |

Each metric reading belongs to a registered device.

The initial schema stores different metric types in a
common readings table.

Metric names and accepted value ranges will be validated
by the application.

The schema may evolve when additional metric types
or device categories are introduced.

## 6. API Design

The following endpoints are proposed for v1.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/v1/devices | Register a device |
| GET | /api/v1/devices | List devices |
| GET | /api/v1/devices/{id} | Retrieve device details |
| POST | /api/v1/metrics | Submit metric readings |
| GET | /api/v1/devices/{id}/metrics/latest | Retrieve latest metrics |
| GET | /api/v1/devices/{id}/metrics | Retrieve historical metrics |

Request and response schemas will be defined during
API implementation.

All timestamps will use UTC.

## 7. Technology Decisions

### Python and FastAPI

FastAPI was selected for the initial backend because
it provides request validation, type-based schemas,
and automatic OpenAPI documentation.

It also provides an opportunity to develop a backend
using Python beyond standalone automation scripts.

### PostgreSQL

PostgreSQL will store device information and metric readings.

The expected initial data volume does not justify
introducing a dedicated time-series database.

Indexing and query performance will be evaluated
after the ingestion workflow is implemented.

### REST APIs

HTTP-based APIs provide a straightforward interface
between the simulator, backend, and future consumers.

An event broker is not required for the initial workflow.

## 8. Error Handling

The API should handle:

- Invalid request payloads
- Unknown device identifiers
- Unsupported metric names
- Metric values outside accepted ranges
- Invalid time ranges
- Database connectivity failures

Validation errors should return appropriate HTTP
status codes with consistent response structures.

Internal exception details must not be exposed
to API consumers.

## 9. Security Considerations

The initial application is intended for local development
using synthetic data.

Basic safeguards include:

- Database credentials supplied through environment variables
- No credentials committed to version control
- Request validation
- Parameterized database queries
- No direct database access from API consumers

Authentication and authorization are outside the initial
implementation scope.

The API must not be exposed publicly without revisiting
these controls.

## 10. Testing Strategy

Testing will focus on:

- Device registration
- Request validation
- Metric ingestion
- Latest-metric retrieval
- Historical time-range queries
- Invalid device and metric handling

Unit tests will cover application logic.

Integration tests will verify API and database behavior.

Performance testing will be introduced after the
end-to-end workflow is operational.

## 11. Known Limitations

The initial architecture does not provide:

- High availability
- Horizontal scaling
- Message queues
- Authentication and authorization
- Real infrastructure integrations
- Distributed collection
- Advanced alerting

These capabilities will be evaluated in later iterations.

## 12. Planned Implementation Sequence

1. Establish FastAPI project structure.
2. Configure PostgreSQL connectivity.
3. Implement device registration.
4. Implement metric ingestion.
5. Build the synthetic metric generator.
6. Implement current and historical metric queries.
7. Add automated tests.
8. Introduce a basic monitoring dashboard.

Architecture decisions will be reviewed as implementation
requirements become clearer.
