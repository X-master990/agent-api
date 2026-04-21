# TrustMesh API Reference

## Agents

### `POST /v1/agents`

Create an agent identity and Ed25519 keypair.

### `GET /v1/agents/{agent_id}`

Fetch a previously created agent.

## Credentials

### `POST /v1/credentials/issue`

Issue a signed capability credential for an agent.

Supported claims:

- `authorized_by`
- `audience`
- `allowed_actions`
- `resource_scope`
- `spending_limit_usd`

### `POST /v1/credentials/verify`

Verify a credential and return an authorization decision.

Checks:

- JWT format
- signature
- expiry
- revocation
- audience
- action
- resource scope
- amount limit

### `POST /v1/credentials/{id}/revoke`

Revoke a credential.

## Audit Logs

### `GET /v1/audit-logs`

List recent verification decisions.

Supported query params:

- `agent_id`
- `result`
- `from`
- `to`
- `limit`
