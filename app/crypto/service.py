import base64
import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from base58 import b58encode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from app.core.config import get_settings

ED25519_MULTICODEC_PREFIX = bytes.fromhex("ed01")


@dataclass(slots=True)
class AgentIdentity:
    did: str
    public_key_bytes: bytes
    private_key_encrypted: bytes


def create_agent_identity() -> AgentIdentity:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return AgentIdentity(
        did=build_did_key(public_key_bytes),
        public_key_bytes=public_key_bytes,
        private_key_encrypted=encrypt_private_key(private_key_bytes),
    )


def build_did_key(public_key_bytes: bytes) -> str:
    encoded = b58encode(ED25519_MULTICODEC_PREFIX + public_key_bytes).decode("ascii")
    return f"did:key:z{encoded}"


def encrypt_private_key(private_key_bytes: bytes) -> bytes:
    return _fernet().encrypt(private_key_bytes)


def decrypt_private_key(private_key_encrypted: bytes) -> Ed25519PrivateKey:
    raw = _fernet().decrypt(private_key_encrypted)
    return Ed25519PrivateKey.from_private_bytes(raw)


def public_key_from_raw(public_key_bytes: bytes) -> Ed25519PublicKey:
    return Ed25519PublicKey.from_public_bytes(public_key_bytes)


def private_key_to_pem(private_key: Ed25519PrivateKey) -> bytes:
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def public_key_to_pem(public_key: Ed25519PublicKey) -> bytes:
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def raw_public_key_to_pem(public_key_bytes: bytes) -> bytes:
    return public_key_to_pem(public_key_from_raw(public_key_bytes))


def issue_spike_jwt(
    issuer: str,
    subject: str,
    claims: dict[str, Any],
    expires_in: int,
) -> tuple[str, str]:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    now = datetime.now(timezone.utc)
    payload = {
        "iss": issuer,
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=expires_in)).timestamp()),
        **claims,
    }
    private_pem = private_key_to_pem(private_key)
    public_pem = public_key_to_pem(public_key)
    token = jwt.encode(payload, private_pem, algorithm="EdDSA")
    return token, public_pem.decode("utf-8")


def verify_spike_jwt(jwt_token: str, public_key_pem: str) -> dict[str, Any]:
    return jwt.decode(
        jwt_token,
        public_key_pem,
        algorithms=["EdDSA"],
        options={"require": ["exp", "iat", "iss", "sub"]},
    )


def _fernet() -> Fernet:
    secret = get_settings().crypto.private_key_encryption_secret.get_secret_value()
    digest = hashlib.sha256(secret.encode("utf-8")).digest()
    return Fernet(base64.urlsafe_b64encode(digest))
