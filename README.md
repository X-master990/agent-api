# TrustMesh

TrustMesh is an agent authorization layer for B2B APIs.

It lets third-party AI agents call your API with verifiable authorization instead of only a shared API key. Your API can answer:

- Who is this agent?
- Who authorized it?
- What actions can it perform?
- Is this request outside the granted scope?

This repository is an MVP backend, Python SDK, and demo for the TrustMesh Agent Authorization Layer.

## What Works

- Agent registration with Ed25519 keypair generation
- `did:key` identity generation
- Capability credential issuance as signed JWTs
- Credential verification with allow / deny decisions
- Policy checks for signature, expiry, revocation, audience, action, resource scope, and amount limit
- Credential revocation
- Audit logs for verification decisions
- Python SDK for local integration
- B2B procurement demo
- Customer-facing browser demo at `/demo`

## Demo Story

Alice Corp has a procurement agent that wants to call Acme's procurement API.

TrustMesh issues a credential saying the agent may:

- call `acme-procurement-api`
- perform `purchase.create` and `catalog.read`
- only act on `vendor_id = acme`
- spend at most `$500` per operation

The demo verifies:

- a valid purchase is allowed
- the wrong vendor is denied
- an over-limit purchase is denied
- an unauthorized action is denied
- every decision appears in audit logs

## Quick Start

```bash
git clone https://github.com/X-master990/agent-api.git
cd agent-api
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
cp .env.example .env
```

Start PostgreSQL, then apply migrations:

```bash
.venv/bin/alembic upgrade head
```

Start the API:

```bash
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Run the demo in another terminal:

```bash
.venv/bin/python -m demos.procurement_demo
```

Or open the customer-facing browser demo:

```text
http://127.0.0.1:8000/demo
```

For detailed setup, see [docs/QUICKSTART.md](./docs/QUICKSTART.md).

## Python SDK

```python
from trustmesh import TrustMesh

tm = TrustMesh(base_url="http://127.0.0.1:8000")

agent = tm.agents.create(
    name="Alice Procurement Agent",
    operator="alice@alicecorp.com",
)

credential = tm.credentials.issue(
    issuer=agent.did,
    subject=agent.did,
    claims={
        "authorized_by": "alice@alicecorp.com",
        "audience": "acme-procurement-api",
        "allowed_actions": ["purchase.create"],
        "resource_scope": {"vendor_id": "acme"},
        "spending_limit_usd": 500,
    },
    expires_in=86400,
)

result = tm.credentials.verify(
    jwt=credential.jwt,
    audience="acme-procurement-api",
    action="purchase.create",
    resource={"vendor_id": "acme"},
    amount_usd=180,
)

print(result.allowed)
```

More examples: [docs/SDK_USAGE.md](./docs/SDK_USAGE.md).

## API Surface

- `POST /v1/agents`
- `GET /v1/agents/{agent_id}`
- `POST /v1/credentials/issue`
- `POST /v1/credentials/verify`
- `POST /v1/credentials/{id}/revoke`
- `GET /v1/audit-logs`
- `GET /demo`

See [docs/API_REFERENCE.md](./docs/API_REFERENCE.md).

## Documentation

- [Quickstart](./docs/QUICKSTART.md)
- [SDK Usage](./docs/SDK_USAGE.md)
- [API Reference](./docs/API_REFERENCE.md)
- [Error Codes](./docs/ERRORS.md)
- [Beta Testing Guide](./docs/BETA_TESTING.md)
- [Customer Interview Guide](./docs/CUSTOMER_INTERVIEW.md)
- [Landing Page Copy](./docs/LANDING.md)
- [GitHub Release Checklist](./docs/GITHUB_RELEASE_CHECKLIST.md)

## Project Timeline

- Week 1: FastAPI skeleton, PostgreSQL schema, agent create/get, Ed25519 + JWT feasibility
- Week 2: Credential issue/revoke/verify, policy checks, audit logs
- Week 3: Python SDK, quickstart, API docs, procurement demo
- Week 4: Beta package, customer validation docs, public repo polish

## MVP Boundaries

This MVP intentionally does not include:

- enterprise SSO
- multi-tenant billing
- OPA/Cedar policy engine
- JSON-LD VC support
- full DID method support beyond `did:key`
- production key management

The current private-key storage is an MVP tradeoff: private keys are encrypted before storage, but future versions should support self-custody or BYOK.

## Development

Run tests:

```bash
.venv/bin/python -m pytest
```

Run the API:

```bash
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```
