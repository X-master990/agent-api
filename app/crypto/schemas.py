from typing import Any

from pydantic import BaseModel, Field


class CryptoSpikeSignRequest(BaseModel):
    issuer: str
    subject: str
    claims: dict[str, Any] = Field(default_factory=dict)
    expires_in: int = Field(default=3600, gt=0, le=604800)


class CryptoSpikeSignResponse(BaseModel):
    jwt: str
    public_key_pem: str


class CryptoSpikeVerifyRequest(BaseModel):
    jwt: str
    public_key_pem: str


class CryptoSpikeVerifyResponse(BaseModel):
    valid: bool
    payload: dict[str, Any] | None
    reason: str | None = None
