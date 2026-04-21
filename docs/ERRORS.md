# TrustMesh Error Codes

TrustMesh verification responses use stable `reason` strings so API teams can make explicit allow / deny decisions and show actionable logs.

## Verification Reasons

### `invalid_jwt`

The supplied JWT cannot be parsed or is missing required fields.

Recommended action:

- Check that the request sends the full JWT string.
- Confirm the token was produced by TrustMesh.

### `issuer_not_found`

The token references an issuer DID that does not exist in TrustMesh.

Recommended action:

- Confirm the issuer agent still exists.
- Reissue the credential using a registered agent.

### `invalid_signature`

The JWT signature cannot be verified with the issuer's public key.

Recommended action:

- Treat the credential as untrusted.
- Do not retry unless a fresh credential is issued.

### `credential_expired`

The credential's `exp` timestamp is in the past.

Recommended action:

- Ask the operator to issue a new credential.

### `credential_not_found`

The JWT has a valid signature but does not match a stored credential record.

Recommended action:

- Reissue the credential through TrustMesh.
- Confirm the verifier is pointed at the correct TrustMesh environment.

### `credential_revoked`

The credential was explicitly revoked.

Recommended action:

- Deny the request.
- Ask the operator to issue a new credential if access should be restored.

### `audience_mismatch`

The credential was issued for a different API audience.

Recommended action:

- Confirm the request's `audience`.
- Issue a credential for the target API.

### `action_not_allowed`

The requested action is not in `allowed_actions`.

Recommended action:

- Deny the request.
- Add the action to a newly issued credential only if the operator approves it.

### `resource_scope_mismatch`

The requested resource does not match the credential's `resource_scope`.

Recommended action:

- Deny the request.
- Confirm resource fields such as `vendor_id`, `account_id`, or `project_id`.

### `amount_limit_exceeded`

The request's `amount_usd` exceeds `spending_limit_usd`.

Recommended action:

- Deny the request.
- Ask for human approval or issue a new credential with a higher limit.

## Successful Response

```json
{
  "valid": true,
  "allowed": true,
  "reason": null,
  "checks": {
    "signature": "valid",
    "expiry": "not_expired",
    "revocation": "not_revoked",
    "audience": "matched",
    "action": "allowed",
    "resource_scope": "matched",
    "amount_limit": "within_limit"
  }
}
```

## Denied Response

```json
{
  "valid": true,
  "allowed": false,
  "reason": "action_not_allowed",
  "checks": {
    "signature": "valid",
    "expiry": "not_expired",
    "revocation": "not_revoked",
    "audience": "matched",
    "action": "denied"
  }
}
```
