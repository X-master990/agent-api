from typing import Any
from uuid import UUID

import httpx

from trustmesh.models import Agent, AuditLog, Credential, VerificationResult


class TrustMeshError(Exception):
    def __init__(self, status_code: int, detail: Any) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"TrustMesh API error {status_code}: {detail}")


class TrustMesh:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "http://127.0.0.1:8000",
        timeout: float = 10.0,
    ) -> None:
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers=headers,
            timeout=timeout,
        )
        self.agents = AgentsClient(self._client)
        self.credentials = CredentialsClient(self._client)
        self.audit_logs = AuditLogsClient(self._client)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "TrustMesh":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AgentsClient:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def create(
        self,
        name: str,
        operator: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Agent:
        response = self._client.post(
            "/v1/agents",
            json={
                "name": name,
                "operator": operator,
                "metadata": metadata or {},
            },
        )
        return Agent.from_api(_json_or_raise(response))

    def get(self, agent_id: str | UUID) -> Agent:
        response = self._client.get(f"/v1/agents/{agent_id}")
        return Agent.from_api(_json_or_raise(response))


class CredentialsClient:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def issue(
        self,
        issuer: str,
        subject: str,
        claims: dict[str, Any],
        expires_in: int = 86400,
    ) -> Credential:
        response = self._client.post(
            "/v1/credentials/issue",
            json={
                "issuer": issuer,
                "subject": subject,
                "claims": claims,
                "expires_in": expires_in,
            },
        )
        return Credential.from_api(_json_or_raise(response))

    def verify(
        self,
        jwt: str,
        audience: str,
        action: str,
        resource: dict[str, Any] | None = None,
        amount_usd: float | None = None,
    ) -> VerificationResult:
        response = self._client.post(
            "/v1/credentials/verify",
            json={
                "jwt": jwt,
                "audience": audience,
                "action": action,
                "resource": resource or {},
                "amount_usd": amount_usd,
            },
        )
        return VerificationResult.from_api(_json_or_raise(response))

    def revoke(self, credential_id: str | UUID) -> dict[str, Any]:
        response = self._client.post(f"/v1/credentials/{credential_id}/revoke")
        return _json_or_raise(response)


class AuditLogsClient:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def list(
        self,
        agent_id: str | None = None,
        result: str | None = None,
        limit: int = 50,
    ) -> list[AuditLog]:
        params: dict[str, Any] = {"limit": limit}
        if agent_id:
            params["agent_id"] = agent_id
        if result:
            params["result"] = result

        response = self._client.get("/v1/audit-logs", params=params)
        return [AuditLog.from_api(item) for item in _json_or_raise(response)]


def _json_or_raise(response: httpx.Response) -> Any:
    if response.is_success:
        return response.json()

    try:
        detail = response.json()
    except ValueError:
        detail = response.text
    raise TrustMeshError(response.status_code, detail)
