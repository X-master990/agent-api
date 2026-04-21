# TrustMesh Beta Testing Guide

This guide is for early testers evaluating whether TrustMesh solves agent access control for B2B APIs.

## What To Test

Run the procurement demo and verify that TrustMesh can:

- register an agent
- issue a capability credential
- allow an in-scope API action
- deny an out-of-scope action
- deny an out-of-scope resource
- deny an over-limit amount
- revoke a credential
- record audit logs for verification decisions

## Setup

```bash
git clone https://github.com/X-master990/agent-api.git
cd agent-api
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
cp .env.example .env
.venv/bin/alembic upgrade head
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
cd agent-api
.venv/bin/python -m demos.procurement_demo
```

## Expected Demo Output

The demo should print results similar to:

```text
valid purchase: True None
wrong vendor: False resource_scope_mismatch
over limit: False amount_limit_exceeded
forbidden action: False action_not_allowed
recent deny audit logs: 5
```

## Evaluation Questions

After testing, answer:

- Was the authorization model easy to understand?
- Were the deny reasons clear enough to debug?
- Would this fit in front of your existing API or middleware?
- Which fields would your API need in `resource_scope`?
- Which actions would you model first?
- Would per-operation spending limits be useful?
- Is audit logging sufficient for staging or production review?
- What is missing before you would try this in staging?

## Report Feedback

Please include:

- your API domain
- one agent workflow you would like to secure
- the actions and resource scopes you would need
- unclear errors or docs
- setup failures
- any security concerns

## Known MVP Limitations

- Local-only setup by default
- No hosted dashboard
- No production API key management yet
- No enterprise SSO
- No BYOK or self-custody key support
- `did:key` only
- Policy checks are fixed and intentionally simple
