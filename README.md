# TrustMesh API

TrustMesh is an agent authorization layer for B2B APIs. This repository contains the MVP backend adapted from `rafsaf/minimal-fastapi-postgres-template` and narrowed to the MVP spec in [TrustMesh_Agent_Authorization_MVP規格書.md](./TrustMesh_Agent_Authorization_MVP規格書.md).

## Week 1 scope

- FastAPI project skeleton
- PostgreSQL schema and Alembic migration
- `POST /v1/agents` to register an agent
- `GET /v1/agents/{agent_id}` to fetch agent details
- Ed25519 + JWT sign/verify spike under `/v1/crypto/spike/*`

## Week 2 scope

- `POST /v1/credentials/issue` to issue capability credentials
- `POST /v1/credentials/{id}/revoke` to revoke credentials
- `POST /v1/credentials/verify` to return allow/deny authorization decisions
- Policy checks for signature, expiry, revocation, audience, action, resource scope, and amount limit
- Verification audit logs written to `verification_logs`
- `GET /v1/audit-logs` to inspect verification decisions

## Week 3 scope

- Python SDK under [`trustmesh/`](./trustmesh)
- Quickstart in [`docs/QUICKSTART.md`](./docs/QUICKSTART.md)
- SDK usage docs in [`docs/SDK_USAGE.md`](./docs/SDK_USAGE.md)
- API reference in [`docs/API_REFERENCE.md`](./docs/API_REFERENCE.md)
- B2B procurement demo in [`demos/procurement_demo.py`](./demos/procurement_demo.py), runnable with `python -m demos.procurement_demo`

## Template source

The current project structure is adapted from the MIT-licensed repository:

- `https://github.com/rafsaf/minimal-fastapi-postgres-template`

The original repo was used as a local reference during scaffolding. The `_vendor/` folder is intentionally ignored and is not part of this repository.

## Quick start

1. Create a virtual environment.
2. Install dependencies from `requirements-dev.txt`.
3. Copy `.env.example` to `.env` and adjust database settings.
4. Run PostgreSQL.
5. Apply migrations with `alembic upgrade head`.
6. Start the API with `uvicorn app.main:app --reload`.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
cp .env.example .env
.venv/bin/alembic upgrade head
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

For a full developer flow, see [`docs/QUICKSTART.md`](./docs/QUICKSTART.md).

## Demo

With the API running:

```bash
.venv/bin/python -m demos.procurement_demo
```

The demo creates an agent, issues a capability credential, verifies allowed and denied requests, and prints recent deny audit logs.

## Implemented API

### Create agent

`POST /v1/agents`

```json
{
  "name": "Alice Procurement Agent",
  "operator": "alice@alicecorp.com",
  "metadata": {
    "team": "procurement"
  }
}
```

The API generates:

- an Ed25519 keypair
- a `did:key` identifier
- an encrypted private key for future credential issuance work

### Get agent

`GET /v1/agents/{agent_id}`

### Crypto spike

- `POST /v1/crypto/spike/sign`
- `POST /v1/crypto/spike/verify`

These endpoints are for Week 1 feasibility work only. They prove Ed25519 signing and JWT verification using ephemeral keys, but they are not the final credential issuance flow for Week 2.

### Credential issue

`POST /v1/credentials/issue`

```json
{
  "issuer": "did:key:z6Mk...",
  "subject": "did:key:z6Mk...",
  "claims": {
    "authorized_by": "alice@alicecorp.com",
    "audience": "acme-procurement-api",
    "allowed_actions": ["purchase.create", "catalog.read"],
    "resource_scope": {
      "vendor_id": "acme"
    },
    "spending_limit_usd": 500
  },
  "expires_in": 86400
}
```

### Credential verify

`POST /v1/credentials/verify`

```json
{
  "jwt": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
  "audience": "acme-procurement-api",
  "action": "purchase.create",
  "resource": {
    "vendor_id": "acme"
  },
  "amount_usd": 180
}
```
