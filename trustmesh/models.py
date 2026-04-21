from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Agent:
    id: str
    did: str
    name: str
    operator: str | None
    metadata: dict[str, Any]
    created_at: str
    status: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Agent":
        return cls(
            id=data["id"],
            did=data["did"],
            name=data["name"],
            operator=data.get("operator"),
            metadata=data.get("metadata", {}),
            created_at=data["created_at"],
            status=data["status"],
        )


@dataclass(slots=True)
class Credential:
    id: str
    issuer: str
    subject: str
    claims: dict[str, Any]
    jwt: str
    issued_at: str
    expires_at: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Credential":
        return cls(
            id=data["id"],
            issuer=data["issuer"],
            subject=data["subject"],
            claims=data["claims"],
            jwt=data["jwt"],
            issued_at=data["issued_at"],
            expires_at=data["expires_at"],
        )


@dataclass(slots=True)
class VerificationResult:
    valid: bool
    allowed: bool
    reason: str | None
    checks: dict[str, str]
    issuer: str | None
    subject: str | None
    claims: dict[str, Any] | None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "VerificationResult":
        return cls(
            valid=data["valid"],
            allowed=data["allowed"],
            reason=data.get("reason"),
            checks=data["checks"],
            issuer=data.get("issuer"),
            subject=data.get("subject"),
            claims=data.get("claims"),
        )


@dataclass(slots=True)
class AuditLog:
    id: str
    credential_id: str | None
    agent_did: str | None
    audience: str | None
    action: str | None
    resource: dict[str, Any] | None
    amount_usd: str | None
    result: str
    reason: str | None
    verified_at: str
    verifier_ip: str | None
    user_agent: str | None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "AuditLog":
        return cls(
            id=data["id"],
            credential_id=data.get("credential_id"),
            agent_did=data.get("agent_did"),
            audience=data.get("audience"),
            action=data.get("action"),
            resource=data.get("resource"),
            amount_usd=data.get("amount_usd"),
            result=data["result"],
            reason=data.get("reason"),
            verified_at=data["verified_at"],
            verifier_ip=data.get("verifier_ip"),
            user_agent=data.get("user_agent"),
        )
