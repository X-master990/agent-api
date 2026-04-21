CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE users (
    id UUID PRIMARY KEY,
    clerk_user_id TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    key_prefix TEXT NOT NULL,
    key_hash TEXT NOT NULL,
    name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    last_used_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ
);

CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    did TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    operator TEXT,
    public_key BYTEA NOT NULL,
    private_key_encrypted BYTEA,
    metadata JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    revoked_at TIMESTAMPTZ
);

CREATE TABLE credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    issuer_did TEXT NOT NULL,
    subject_did TEXT NOT NULL,
    claims JSONB NOT NULL,
    jwt TEXT NOT NULL,
    issued_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    expires_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ
);

CREATE TABLE verification_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    credential_id UUID REFERENCES credentials(id),
    agent_did TEXT,
    audience TEXT,
    action TEXT,
    resource JSONB,
    amount_usd NUMERIC(10, 2),
    result TEXT NOT NULL,
    reason TEXT,
    verified_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    verifier_ip TEXT,
    user_agent TEXT
);

CREATE INDEX idx_agents_did ON agents(did);
CREATE INDEX idx_credentials_subject ON credentials(subject_did);
CREATE INDEX idx_credentials_issuer ON credentials(issuer_did);
CREATE INDEX idx_verification_logs_time ON verification_logs(verified_at DESC);
