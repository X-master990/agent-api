# TrustMesh Landing Page Copy

## Hero

Let AI agents call your API with verifiable authorization, not just an API key.

TrustMesh is an authorization layer for B2B APIs that need to safely accept third-party AI agents. Verify who the agent is, who authorized it, what it can do, and whether each request is in scope.

## Primary CTA

Try the local MVP

## Secondary CTA

Run the procurement demo

## Problem

AI agents are starting to call B2B APIs, but most APIs still rely on shared API keys or user tokens.

That leaves teams asking:

- Which agent made this call?
- Who authorized it?
- What was it allowed to do?
- Was this request outside scope?
- Can we revoke it?
- Can we audit what happened?

## Solution

TrustMesh issues signed capability credentials to agents and verifies every API request against explicit authorization rules.

Each credential can define:

- API audience
- allowed actions
- resource scope
- per-operation amount limit
- expiration
- revocation status

## How It Works

1. Register an agent.
2. Issue a signed capability credential.
3. Agent calls your API with the credential.
4. Your API asks TrustMesh to verify the request.
5. TrustMesh returns `allow` or `deny` with a reason.
6. Every decision is stored in audit logs.

## Example

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

## Use Cases

- procurement APIs
- refund and payment APIs
- CRM automation
- support workflow automation
- data export APIs
- partner API access

## Not Another Observability Tool

TrustMesh is not a tracing dashboard, LLM gateway, or token cost monitor.

It focuses on authorization decisions:

- identity
- delegation
- scope
- revocation
- audit

## Current MVP

The MVP includes:

- FastAPI backend
- PostgreSQL schema
- Ed25519 signed credentials
- `did:key` agent identity
- Python SDK
- procurement demo
- browser-based customer demo
- audit logs

## CTA Footer

Clone the repo and run the local demo in under 10 minutes.
