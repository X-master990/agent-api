"""initial_trustmesh_week1

Revision ID: 20260420_2120
Revises:
Create Date: 2026-04-20 21:20:00

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "20260420_2120"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("clerk_user_id", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("clerk_user_id"),
    )
    op.create_table(
        "api_keys",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("key_prefix", sa.Text(), nullable=False),
        sa.Column("key_hash", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "agents",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("did", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("operator", sa.Text(), nullable=True),
        sa.Column("public_key", sa.LargeBinary(), nullable=False),
        sa.Column("private_key_encrypted", sa.LargeBinary(), nullable=True),
        sa.Column(
            "metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("did"),
    )
    op.create_table(
        "credentials",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("issuer_did", sa.Text(), nullable=False),
        sa.Column("subject_did", sa.Text(), nullable=False),
        sa.Column(
            "claims",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("jwt", sa.Text(), nullable=False),
        sa.Column(
            "issued_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "verification_logs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("credential_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("agent_did", sa.Text(), nullable=True),
        sa.Column("audience", sa.Text(), nullable=True),
        sa.Column("action", sa.Text(), nullable=True),
        sa.Column(
            "resource",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("amount_usd", sa.Numeric(10, 2), nullable=True),
        sa.Column("result", sa.Text(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "verified_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("verifier_ip", sa.Text(), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["credential_id"], ["credentials.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_agents_did", "agents", ["did"], unique=False)
    op.create_index(
        "idx_credentials_subject", "credentials", ["subject_did"], unique=False
    )
    op.create_index(
        "idx_credentials_issuer", "credentials", ["issuer_did"], unique=False
    )
    op.create_index(
        "idx_verification_logs_time",
        "verification_logs",
        ["verified_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("idx_verification_logs_time", table_name="verification_logs")
    op.drop_index("idx_credentials_issuer", table_name="credentials")
    op.drop_index("idx_credentials_subject", table_name="credentials")
    op.drop_index("idx_agents_did", table_name="agents")
    op.drop_table("verification_logs")
    op.drop_table("credentials")
    op.drop_table("agents")
    op.drop_table("api_keys")
    op.drop_table("users")
