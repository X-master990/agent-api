import os

from trustmesh import TrustMesh


def main() -> None:
    tm = TrustMesh(base_url=os.getenv("TRUSTMESH_BASE_URL", "http://127.0.0.1:8000"))

    agent = tm.agents.create(
        name="Alice Procurement Agent",
        operator="alice@alicecorp.com",
        metadata={"team": "procurement"},
    )
    print(f"agent: {agent.id} {agent.did}")

    credential = tm.credentials.issue(
        issuer=agent.did,
        subject=agent.did,
        claims={
            "authorized_by": "alice@alicecorp.com",
            "audience": "acme-procurement-api",
            "allowed_actions": ["purchase.create", "catalog.read"],
            "resource_scope": {"vendor_id": "acme"},
            "spending_limit_usd": 500,
        },
        expires_in=86400,
    )
    print(f"credential: {credential.id}")

    allowed = tm.credentials.verify(
        jwt=credential.jwt,
        audience="acme-procurement-api",
        action="purchase.create",
        resource={"vendor_id": "acme"},
        amount_usd=180,
    )
    print("valid purchase:", allowed.allowed, allowed.reason, allowed.checks)

    wrong_vendor = tm.credentials.verify(
        jwt=credential.jwt,
        audience="acme-procurement-api",
        action="purchase.create",
        resource={"vendor_id": "other-vendor"},
        amount_usd=180,
    )
    print("wrong vendor:", wrong_vendor.allowed, wrong_vendor.reason)

    over_limit = tm.credentials.verify(
        jwt=credential.jwt,
        audience="acme-procurement-api",
        action="purchase.create",
        resource={"vendor_id": "acme"},
        amount_usd=999,
    )
    print("over limit:", over_limit.allowed, over_limit.reason)

    forbidden_action = tm.credentials.verify(
        jwt=credential.jwt,
        audience="acme-procurement-api",
        action="purchase.delete",
        resource={"vendor_id": "acme"},
        amount_usd=180,
    )
    print("forbidden action:", forbidden_action.allowed, forbidden_action.reason)

    deny_logs = tm.audit_logs.list(result="deny", limit=5)
    print(f"recent deny audit logs: {len(deny_logs)}")
    for log in deny_logs:
        print(f"- {log.action}: {log.reason} at {log.verified_at}")


if __name__ == "__main__":
    main()
