from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CapabilityClaims(BaseModel):
    authorized_by: str
    audience: str
    allowed_actions: list[str] = Field(min_length=1)
    resource_scope: dict[str, Any] = Field(default_factory=dict)
    spending_limit_usd: float | None = Field(default=None, ge=0)


class CredentialIssueRequest(BaseModel):
    subject: str
    issuer: str
    claims: CapabilityClaims
    expires_in: int = Field(gt=0, le=30 * 24 * 60 * 60)


class CredentialIssueResponse(BaseModel):
    id: UUID
    issuer: str
    subject: str
    claims: CapabilityClaims
    jwt: str
    issued_at: datetime
    expires_at: datetime


class CredentialVerifyRequest(BaseModel):
    jwt: str
    audience: str
    action: str
    resource: dict[str, Any] = Field(default_factory=dict)
    amount_usd: float | None = Field(default=None, ge=0)


class CredentialVerifyResponse(BaseModel):
    valid: bool
    allowed: bool
    reason: str | None
    checks: dict[str, str]
    issuer: str | None = None
    subject: str | None = None
    claims: dict[str, Any] | None = None


class CredentialRevokeResponse(BaseModel):
    id: UUID
    revoked_at: datetime


class CredentialRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    issuer_did: str
    subject_did: str
    claims: dict[str, Any]
    jwt: str
    issued_at: datetime
    expires_at: datetime | None
    revoked_at: datetime | None
