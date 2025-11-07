<!-- omit in toc -->
# Backend

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
[![CI](https://github.com/Astro-BEAM-AUTh/backend/workflows/CI/badge.svg)](https://github.com/Astro-BEAM-AUTh/backend/actions)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

<!-- omit in toc -->
## Table of Contents
- [Overview](#overview)
- [How to Run](#how-to-run)
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

## Development
To install the development dependencies, run:

```bash
uv sync --dev
```

## Contributing

Contributions are welcome!
If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

Please read our [Contributing Guidelines](https://github.com/Astro-BEAM-AUTh/telescope-data-handler?tab=contributing-ov-file) for more details.