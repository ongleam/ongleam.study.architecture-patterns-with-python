# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a study project for "Architecture Patterns with Python" (Cosmic Python) book by Harry Percival and Bob Gregory. The project implements an allocation domain for an online furniture retailer, demonstrating Domain-Driven Design (DDD) patterns.

## Tech Stack

- **Python 3.11+**
- **FastAPI** - Web framework for REST API entrypoints
- **SQLAlchemy 2.0** - ORM and database abstraction (classical mapping style)
- **Pydantic 2.0** - Request/response validation
- **pytest** - Testing framework
- **uv** - Package manager

## Commands

```bash
# Install dependencies (using uv)
uv sync

# Install with dev dependencies
uv sync --extra dev

# Run all tests
uv run pytest

# Run specific test types
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest tests/e2e/

# Run a single test file
uv run pytest tests/unit/test_model.py

# Run a single test function
uv run pytest tests/unit/test_model.py::test_function_name -v
```

## Architecture

This project follows Clean Architecture / Hexagonal Architecture principles from the book:

### Directory Structure (Target)

```
src/allocation/
├── domain/           # Domain model (entities, value objects, domain services)
│   └── model.py
├── adapters/         # Infrastructure adapters (repository, ORM)
│   ├── orm.py
│   └── repository.py
├── service_layer/    # Application services (use cases)
│   └── services.py
├── entrypoints/      # API layer (FastAPI)
│   └── api.py
└── config.py         # Environment configuration
```

### Key Patterns

- **Domain Model**: Pure Python classes with business logic, no framework dependencies
- **Repository Pattern**: Abstract persistence, domain model doesn't know about database
- **Service Layer**: Orchestrates use cases, transaction boundaries
- **Unit of Work**: Manages atomic operations across repositories
- **Dependency Injection**: Wire up adapters at runtime

### Test Pyramid

- `tests/unit/`: Domain model tests, no I/O
- `tests/integration/`: Repository and ORM tests with database
- `tests/e2e/`: API tests against running application

### Dependency Rule

Dependencies flow inward: `entrypoints → service_layer → domain ← adapters`

The domain model has no dependencies on outer layers.

## Study Materials

Chapter-by-chapter study materials are in `assets/markdown/`:

- `ch01-domain-modeling.md` - Domain Model, Entity, Value Object
- `ch02-repository-pattern.md` - Repository Pattern
- `ch03-coupling-and-abstractions.md` - Abstractions and Coupling
- `ch04-flask-api-service-layer.md` - Service Layer
- And more...
