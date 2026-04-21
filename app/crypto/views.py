from fastapi import APIRouter, HTTPException
from jwt import InvalidTokenError

from app.crypto.schemas import (
    CryptoSpikeSignRequest,
    CryptoSpikeSignResponse,
    CryptoSpikeVerifyRequest,
    CryptoSpikeVerifyResponse,
)
from app.crypto.service import issue_spike_jwt, verify_spike_jwt

router = APIRouter()


@router.post("/spike/sign", response_model=CryptoSpikeSignResponse)
async def sign_spike_jwt(
    payload: CryptoSpikeSignRequest,
) -> CryptoSpikeSignResponse:
    token, public_key_pem = issue_spike_jwt(
        issuer=payload.issuer,
        subject=payload.subject,
        claims=payload.claims,
        expires_in=payload.expires_in,
    )
    return CryptoSpikeSignResponse(jwt=token, public_key_pem=public_key_pem)


@router.post("/spike/verify", response_model=CryptoSpikeVerifyResponse)
async def verify_signed_spike_jwt(
    payload: CryptoSpikeVerifyRequest,
) -> CryptoSpikeVerifyResponse:
    try:
        decoded = verify_spike_jwt(payload.jwt, payload.public_key_pem)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=400, detail=f"invalid_token:{exc}") from exc

    return CryptoSpikeVerifyResponse(valid=True, payload=decoded)
