<!-- omit in toc -->
# Backend

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
[![CI](https://github.com/Astro-BEAM-AUTh/backend/workflows/CI/badge.svg)](https://github.com/Astro-BEAM-AUTh/backend/actions)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

<!-- omit in toc -->
## Table of Contents
- [Overview](#overview)
- [How to Run](#how-to-run)
- [Database Management](#database-management)
- [Development](#development)
- [Contributing](#contributing)

## Overview
This project is responsible for the backend services of the Astro-BEAM-AUTh application.
It manages the following tasks:
- Handling API requests and responses.
- Managing user authentication and authorization.
- Interfacing with the database for data storage and retrieval.
- Managing telescope observations and scheduling.

## How to Run
To run the backend, execute the following command:

```bash
uv run backend
```

## Database Management
Database lifecycle is managed from this project using Alembic migrations.

Initialize the database and apply all migrations:

```bash
uv run backend-db init
```

Apply pending migrations:

```bash
uv run backend-db upgrade
```

Create a new migration from model changes:

```bash
uv run backend-db revision -m "describe change" --autogenerate
```

Each created revision also generates SQL artifacts in `migrations/versions/sql`:
- `<revision_id>_upgrade.sql`
- `<revision_id>_downgrade.sql`

If you want to skip SQL artifact generation for a specific revision:

```bash
uv run backend-db revision -m "describe change" --autogenerate --no-sql
```

By default, revision IDs are generated as `YYYYMMDD_NNNN`.
For example, the first revision on 2026-05-05 is `20260505_0001`.
You can still override manually:

```bash
uv run backend-db revision -m "describe change" --autogenerate --rev-id 20260505_0009
```

Inspect migration state:

```bash
uv run backend-db current
uv run backend-db history
```

## Development
To install the development dependencies, run:

```bash
uv sync --dev
```

## Contributing

Contributions are welcome!
If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

Please read our [Contributing Guidelines](https://github.com/Astro-BEAM-AUTh/backend?tab=contributing-ov-file) for more details.