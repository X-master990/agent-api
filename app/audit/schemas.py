from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VerificationLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    credential_id: UUID | None
    agent_did: str | None
    audience: str | None
    action: str | None
    resource: dict[str, Any] | None
    amount_usd: Decimal | None
    result: str
    reason: str | None
    verified_at: datetime
    verifier_ip: str | None
    user_agent: str | None
