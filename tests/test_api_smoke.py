from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_live_probe() -> None:
    response = client.get("/probe/live")
    assert response.status_code == 200
    assert response.json() == "ok"


def test_crypto_spike_roundtrip() -> None:
    sign_response = client.post(
        "/v1/crypto/spike/sign",
        json={
            "issuer": "did:key:zIssuer",
            "subject": "did:key:zSubject",
            "claims": {"audience": "acme-procurement-api"},
            "expires_in": 300,
        },
    )
    assert sign_response.status_code == 200
    signed = sign_response.json()

    verify_response = client.post(
        "/v1/crypto/spike/verify",
        json={
            "jwt": signed["jwt"],
            "public_key_pem": signed["public_key_pem"],
        },
    )
    assert verify_response.status_code == 200
    verified = verify_response.json()

    assert verified["valid"] is True
    assert verified["payload"]["audience"] == "acme-procurement-api"
