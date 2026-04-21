# TrustMesh Python SDK

The SDK wraps the local REST API with small Python clients.

## Client

```python
from trustmesh import TrustMesh

tm = TrustMesh(base_url="http://127.0.0.1:8000")
```

## Agents

```python
agent = tm.agents.create(
    name="Alice Procurement Agent",
    operator="alice@alicecorp.com",
    metadata={"team": "procurement"},
)

same_agent = tm.agents.get(agent.id)
```

## Credentials

```python
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
```

```python
result = tm.credentials.verify(
    jwt=credential.jwt,
    audience="acme-procurement-api",
    action="purchase.create",
    resource={"vendor_id": "acme"},
    amount_usd=180,
)

if result.allowed:
    print("allow")
else:
    print(result.reason)
```

```python
tm.credentials.revoke(credential.id)
```

## Audit Logs

```python
deny_logs = tm.audit_logs.list(result="deny", limit=10)
```
