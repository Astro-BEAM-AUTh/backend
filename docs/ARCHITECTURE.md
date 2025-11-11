<!-- omit in toc -->
# Architecture Diagram

<!-- omit in toc -->
## Table of Contents
- [Request Flow](#request-flow)
  - [1. Submit Observation Request](#1-submit-observation-request)
  - [2. Get Web Data](#2-get-web-data)
- [Technology Stack](#technology-stack)
- [Security Considerations (Future)](#security-considerations-future)


## Request Flow

### 1. Submit Observation Request

```
Client
  │
  │ POST /telescope/observations
  │ { target_name, ra, dec, ... }
  │
  ▼
FastAPI Router (telescope.py)
  │
  │ 1. Validate with Pydantic
  │ 2. Generate observation_id
  │
  ▼
Kafka Handler
  │
  │ Send to Kafka topic
  │
  ▼
Kafka Broker
  │
  │ Store in topic "telescope-observations"
  │
  ▼
Response to Client
  │
  │ { observation_id, status: "pending", ... }
  │
  ▼
Client receives confirmation
```

### 2. Get Web Data

```
Client
  │
  │ GET /web/status
  │
  ▼
FastAPI Router (web.py)
  │
  │ 1. Validate request
  │ 2. Query database (future)
  │
  ▼
Database (PostgreSQL)
  │
  │ SELECT * FROM telescope_observations
  │
  ▼
Response to Client
  │
  │ { status, data, ... }
  │
  ▼
Client receives data
```

## Technology Stack

```
┌────────────────────────────────────────┐
│         Application Layer              │
│                                        │
│  FastAPI 0.121+ (Async Web Framework)  │
│  Uvicorn (ASGI Server)                 │
│  Pydantic 2.10+ (Validation)           │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│          Data Layer                    │
│                                        │
│  SQLAlchemy 2.0+ (Async ORM)           │
│  asyncpg (PostgreSQL Driver)           │
│  PostgreSQL 16+ (Database)             │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│       Messaging Layer                  │
│                                        │
│  aiokafka (Kafka Client)               │
│  Apache Kafka (Message Broker)         │
└────────────────────────────────────────┘
```

## Security Considerations (Future)

- [ ] API Key authentication
- [ ] JWT tokens
- [ ] Rate limiting
- [ ] Input sanitization (Pydantic handles this)
- [ ] SQL injection protection (SQLAlchemy handles this)
- [ ] HTTPS/TLS
- [ ] CORS configuration
- [ ] Request validation
- [ ] Error message sanitization
