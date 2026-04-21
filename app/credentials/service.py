from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any
from uuid import UUID

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.models import Agent
from app.audit.models import VerificationLog
from app.credentials.models import Credential
from app.credentials.schemas import (
    CapabilityClaims,
    CredentialIssueRequest,
    CredentialVerifyRequest,
    CredentialVerifyResponse,
)
from app.crypto.service import (
    decrypt_private_key,
    private_key_to_pem,
    raw_public_key_to_pem,
)


class CredentialError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


async def issue_credential(
    session: AsyncSession,
    payload: CredentialIssueRequest,
) -> Credential:
    issuer_agent = await session.scalar(
        select(Agent).where(Agent.did == payload.issuer, Agent.revoked_at.is_(None))
    )
    if issuer_agent is None:
        raise CredentialError("issuer_not_found")

    subject_agent = await session.scalar(
        select(Agent).where(Agent.did == payload.subject, Agent.revoked_at.is_(None))
    )
    if subject_agent is None:
        raise CredentialError("subject_not_found")

    if issuer_agent.private_key_encrypted is None:
        raise CredentialError("issuer_private_key_unavailable")

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=payload.expires_in)
    claims = payload.claims.model_dump(mode="json")
    token_payload = {
        "iss": payload.issuer,
        "sub": payload.subject,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
        **claims,
    }
    private_key = decrypt_private_key(issuer_agent.private_key_encrypted)
    token = jwt.encode(token_payload, private_key_to_pem(private_key), algorithm="EdDSA")

    credential = Credential(
        issuer_did=payload.issuer,
        subject_did=payload.subject,
        claims=claims,
        jwt=token,
        expires_at=expires_at,
    )
    session.add(credential)
    await session.commit()
    await session.refresh(credential)
    return credential


async def revoke_credential(session: AsyncSession, credential_id: UUID) -> Credential:
    credential = await session.get(Credential, credential_id)
    if credential is None:
        raise CredentialError("credential_not_found")

    if credential.revoked_at is None:
        credential.revoked_at = datetime.now(timezone.utc)
        session.add(credential)
        await session.commit()
        await session.refresh(credential)

    return credential


async def verify_credential(
    session: AsyncSession,
    payload: CredentialVerifyRequest,
    verifier_ip: str | None = None,
    user_agent: str | None = None,
) -> CredentialVerifyResponse:
    checks: dict[str, str] = {}
    credential: Credential | None = None
    decoded: dict[str, Any] | None = None

    try:
        unverified = jwt.decode(payload.jwt, options={"verify_signature": False})
        issuer = unverified.get("iss")
        subject = unverified.get("sub")
        if not isinstance(issuer, str) or not isinstance(subject, str):
            checks["format"] = "invalid"
            return await _deny_and_log(
                session,
                payload,
                "invalid_jwt",
                checks,
                credential,
                decoded,
                verifier_ip,
                user_agent,
                valid=False,
            )
        checks["format"] = "valid"
    except InvalidTokenError:
        checks["format"] = "invalid"
        return await _deny_and_log(
            session,
            payload,
            "invalid_jwt",
            checks,
            credential,
            decoded,
            verifier_ip,
            user_agent,
            valid=False,
        )

    issuer_agent = await session.scalar(select(Agent).where(Agent.did == issuer))
    if issuer_agent is None:
        checks["signature"] = "issuer_not_found"
        return await _deny_and_log(
            session,
            payload,
            "issuer_not_found",
            checks,
            credential,
            decoded,
            verifier_ip,
            user_agent,
            valid=False,
        )

    try:
        decoded = jwt.decode(
            payload.jwt,
            raw_public_key_to_pem(issuer_agent.public_key),
            algorithms=["EdDSA"],
            options={"require": ["exp", "iat", "iss", "sub"]},
        )
        checks["signature"] = "valid"
        checks["expiry"] = "not_expired"
    except ExpiredSignatureError:
        checks["signature"] = "valid"
        checks["expiry"] = "expired"
        return await _deny_and_log(
            session,
            payload,
            "credential_expired",
            checks,
            credential,
            decoded,
            verifier_ip,
            user_agent,
            valid=False,
        )
    except InvalidTokenError:
        checks["signature"] = "invalid"
        return await _deny_and_log(
            session,
            payload,
            "invalid_signature",
            checks,
            credential,
            decoded,
            verifier_ip,
            user_agent,
            valid=False,
        )

    credential = await session.scalar(select(Credential).where(Credential.jwt == payload.jwt))
    if credential is None:
        checks["revocation"] = "credential_not_found"
        return await _deny_and_log(
            session,
            payload,
            "credential_not_found",
            checks,
            credential,
            decoded,
            verifier_ip,
            user_agent,
            valid=False,
        )

    if credential.revoked_at is not None:
        checks["revocation"] = "revoked"
        return await _deny_and_log(
            session,
            payload,
            "credential_revoked",
            checks,
            credential,
            decoded,
            verifier_ip,
            user_agent,
        )
    checks["revocation"] = "not_revoked"

    claims = CapabilityClaims.model_validate(
        {key: decoded.get(key) for key in CapabilityClaims.model_fields}
    )

    if claims.audience != payload.audience:
        checks["audience"] = "mismatched"
        return await _deny_and_log(
            session,
            payload,
            "audience_mismatch",
            checks,
            credential,
            decoded,
            verifier_ip,
            user_agent,
        )
    checks["audience"] = "matched"

    if payload.action not in claims.allowed_actions:
        checks["action"] = "denied"
        return await _deny_and_log(
            session,
            payload,
            "action_not_allowed",
            checks,
            credential,
            decoded,
            verifier_ip,
            user_agent,
        )
    checks["action"] = "allowed"

    if not _resource_matches(claims.resource_scope, payload.resource):
        checks["resource_scope"] = "mismatched"
        return await _deny_and_log(
            session,
            payload,
            "resource_scope_mismatch",
            checks,
            credential,
            decoded,
            verifier_ip,
            user_agent,
        )
    checks["resource_scope"] = "matched"

    if claims.spending_limit_usd is not None and payload.amount_usd is not None:
        if payload.amount_usd > claims.spending_limit_usd:
            checks["amount_limit"] = "exceeded"
            return await _deny_and_log(
                session,
                payload,
                "amount_limit_exceeded",
                checks,
                credential,
                decoded,
                verifier_ip,
                user_agent,
            )
        checks["amount_limit"] = "within_limit"
    else:
        checks["amount_limit"] = "skipped"

    await _write_audit_log(
        session,
        payload,
        credential,
        result="allow",
        reason=None,
        verifier_ip=verifier_ip,
        user_agent=user_agent,
    )
    return CredentialVerifyResponse(
        valid=True,
        allowed=True,
        reason=None,
        checks=checks,
        issuer=decoded.get("iss"),
        subject=decoded.get("sub"),
        claims=credential.claims,
    )


def _resource_matches(
    resource_scope: dict[str, Any],
    request_resource: dict[str, Any],
) -> bool:
    return all(request_resource.get(key) == value for key, value in resource_scope.items())


async def _deny_and_log(
    session: AsyncSession,
    payload: CredentialVerifyRequest,
    reason: str,
    checks: dict[str, str],
    credential: Credential | None,
    decoded: dict[str, Any] | None,
    verifier_ip: str | None,
    user_agent: str | None,
    valid: bool = True,
) -> CredentialVerifyResponse:
    await _write_audit_log(
        session,
        payload,
        credential,
        result="deny",
        reason=reason,
        verifier_ip=verifier_ip,
        user_agent=user_agent,
    )
    return CredentialVerifyResponse(
        valid=valid,
        allowed=False,
        reason=reason,
        checks=checks,
        issuer=decoded.get("iss") if decoded else None,
        subject=decoded.get("sub") if decoded else None,
        claims=credential.claims if credential else None,
    )


async def _write_audit_log(
    session: AsyncSession,
    payload: CredentialVerifyRequest,
    credential: Credential | None,
    result: str,
    reason: str | None,
    verifier_ip: str | None,
    user_agent: str | None,
) -> None:
    session.add(
        VerificationLog(
            credential_id=credential.id if credential else None,
            agent_did=credential.subject_did if credential else None,
            audience=payload.audience,
            action=payload.action,
            resource=payload.resource,
            amount_usd=payload.amount_usd,
            result=result,
            reason=reason,
            verifier_ip=verifier_ip,
            user_agent=user_agent,
        )
    )
    await session.commit()
