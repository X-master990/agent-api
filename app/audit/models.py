import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base


class VerificationLog(Base):
    __tablename__ = "verification_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    )
    credential_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), sa.ForeignKey("credentials.id"), nullable=True
    )
    agent_did: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    audience: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    action: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    resource: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    amount_usd: Mapped[Decimal | None] = mapped_column(sa.Numeric(10, 2), nullable=True)
    result: Mapped[str] = mapped_column(sa.Text, nullable=False)
    reason: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    verified_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )
    verifier_ip: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
