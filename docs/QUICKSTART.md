# TrustMesh Quickstart

This quickstart runs the Week 3 developer flow with the local API and Python SDK.

## 1. Start PostgreSQL

```bash
~/Applications/Postgres.app/Contents/Versions/16/bin/pg_ctl -D "$HOME/Library/Application Support/Postgres/var-16" -l "$HOME/Library/Logs/Postgres/postgres-16.log" start
```

If it is already running, this command may say another server is running. Check status instead:

```bash
~/Applications/Postgres.app/Contents/Versions/16/bin/pg_isready -h 127.0.0.1 -p 5432
```

## 2. Apply migrations

```bash
cd "/Users/b/Desktop/ai agent security"
.venv/bin/alembic upgrade head
```

## 3. Start the API

```bash
cd "/Users/b/Desktop/ai agent security"
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open the docs:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/demo`

## 4. Run the procurement demo

In another terminal:

```bash
cd "/Users/b/Desktop/ai agent security"
.venv/bin/python -m demos.procurement_demo
```

If your API is not running on port `8000`, set `TRUSTMESH_BASE_URL`:

```bash
TRUSTMESH_BASE_URL=http://127.0.0.1:8001 .venv/bin/python -m demos.procurement_demo
```

Expected output includes:

```text
valid purchase: True None
wrong vendor: False resource_scope_mismatch
over limit: False amount_limit_exceeded
forbidden action: False action_not_allowed
```

For a customer-facing visual demo, open:

```text
http://127.0.0.1:8000/demo
```

Click `Run full authorization demo` to create an agent, issue a credential, verify allowed and denied requests, and show audit logs.

## 5. Use the SDK directly

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
