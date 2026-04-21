from trustmesh.models import Agent, AuditLog, Credential, VerificationResult


def test_agent_model_from_api() -> None:
    agent = Agent.from_api(
        {
            "id": "ag_1",
            "did": "did:key:zabc",
            "name": "Agent",
            "operator": "alice@example.com",
            "metadata": {"team": "procurement"},
            "created_at": "2026-04-21T00:00:00Z",
            "status": "active",
        }
    )
    assert agent.did == "did:key:zabc"
    assert agent.metadata["team"] == "procurement"


def test_credential_model_from_api() -> None:
    credential = Credential.from_api(
        {
            "id": "cred_1",
            "issuer": "did:key:zissuer",
            "subject": "did:key:zsubject",
            "claims": {"audience": "acme"},
            "jwt": "token",
            "issued_at": "2026-04-21T00:00:00Z",
            "expires_at": "2026-04-22T00:00:00Z",
        }
    )
    assert credential.issuer == "did:key:zissuer"
    assert credential.claims["audience"] == "acme"


def test_verification_result_model_from_api() -> None:
    result = VerificationResult.from_api(
        {
            "valid": True,
            "allowed": False,
            "reason": "action_not_allowed",
            "checks": {"action": "denied"},
            "issuer": "did:key:zissuer",
            "subject": "did:key:zsubject",
            "claims": {"audience": "acme"},
        }
    )
    assert result.valid is True
    assert result.allowed is False
    assert result.reason == "action_not_allowed"


def test_audit_log_model_from_api() -> None:
    log = AuditLog.from_api(
        {
            "id": "log_1",
            "credential_id": "cred_1",
            "agent_did": "did:key:zagent",
            "audience": "acme",
            "action": "purchase.create",
            "resource": {"vendor_id": "acme"},
            "amount_usd": "180.00",
            "result": "allow",
            "reason": None,
            "verified_at": "2026-04-21T00:00:00Z",
            "verifier_ip": "127.0.0.1",
            "user_agent": "pytest",
        }
    )
    assert log.result == "allow"
    assert log.resource == {"vendor_id": "acme"}
