import uuid
from datetime import datetime
from typing import Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True
    )
    did: Mapped[str] = mapped_column(sa.Text, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(sa.Text, nullable=False)
    operator: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    public_key: Mapped[bytes] = mapped_column(sa.LargeBinary, nullable=False)
    private_key_encrypted: Mapped[bytes | None] = mapped_column(
        sa.LargeBinary, nullable=True
    )
    metadata_json: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        default=dict,
        server_default=sa.text("'{}'::jsonb"),
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
