from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database_session import new_async_session
from app.credentials.schemas import (
    CredentialIssueRequest,
    CredentialIssueResponse,
    CredentialRevokeResponse,
    CredentialVerifyRequest,
    CredentialVerifyResponse,
)
from app.credentials.service import (
    CredentialError,
    issue_credential,
    revoke_credential,
    verify_credential,
)

router = APIRouter()


@router.post(
    "/issue",
    response_model=CredentialIssueResponse,
    status_code=status.HTTP_201_CREATED,
)
async def issue_capability_credential(
    payload: CredentialIssueRequest,
    session: AsyncSession = Depends(new_async_session),
) -> CredentialIssueResponse:
    try:
        credential = await issue_credential(session, payload)
    except CredentialError as exc:
        raise HTTPException(status_code=400, detail=exc.reason) from exc

    assert credential.expires_at is not None
    return CredentialIssueResponse(
        id=credential.id,
        issuer=credential.issuer_did,
        subject=credential.subject_did,
        claims=payload.claims,
        jwt=credential.jwt,
        issued_at=credential.issued_at,
        expires_at=credential.expires_at,
    )


@router.post("/{credential_id}/revoke", response_model=CredentialRevokeResponse)
async def revoke_capability_credential(
    credential_id: UUID,
    session: AsyncSession = Depends(new_async_session),
) -> CredentialRevokeResponse:
    try:
        credential = await revoke_credential(session, credential_id)
    except CredentialError as exc:
        raise HTTPException(status_code=404, detail=exc.reason) from exc

    assert credential.revoked_at is not None
    return CredentialRevokeResponse(id=credential.id, revoked_at=credential.revoked_at)


@router.post("/verify", response_model=CredentialVerifyResponse)
async def verify_capability_credential(
    payload: CredentialVerifyRequest,
    request: Request,
    session: AsyncSession = Depends(new_async_session),
) -> CredentialVerifyResponse:
    return await verify_credential(
        session,
        payload,
        verifier_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
