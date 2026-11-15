# ADR 0001: Modular Monolith

- Status: Accepted
- Date: 2026-11-15

## Context

The platform requires ingestion, APIs, risk analysis, graph intelligence, investigation workflows, and a separate web client. There is not yet evidence that independently deployed services are necessary.

## Decision

Use a modular monolith consisting of a React frontend, FastAPI backend, PostgreSQL persistence, and explicit Python domain modules. Use Docker Compose for local development.

## Consequences

This reduces deployment and debugging complexity. It requires discipline to maintain module boundaries and avoid tightly coupled route handlers.

Revisit this decision when measured throughput, availability, scaling, or team ownership requirements justify service extraction.
