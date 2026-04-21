import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.agents.views import router as agents_router
from app.audit.views import router as audit_router
from app.core import lifespan
from app.core.config import get_settings
import app.core.model_registry  # noqa: F401
from app.credentials.views import router as credentials_router
from app.crypto.views import router as crypto_router
from app.demo.views import router as demo_router
from app.probe.views import router as probe_router

logger = logging.getLogger(__name__)


app = FastAPI(
    title="TrustMesh API",
    version="0.2.0",
    description="TrustMesh Agent Authorization Layer MVP",
    openapi_url="/openapi.json",
    docs_url="/docs",
    lifespan=lifespan.lifespan,
)

app.include_router(agents_router, prefix="/v1/agents", tags=["agents"])
app.include_router(credentials_router, prefix="/v1/credentials", tags=["credentials"])
app.include_router(audit_router, prefix="/v1/audit-logs", tags=["audit logs"])
app.include_router(crypto_router, prefix="/v1/crypto", tags=["crypto"])
app.include_router(demo_router, prefix="/demo", tags=["demo"])
app.include_router(probe_router, prefix="/probe", tags=["probe"])

# Sets all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(origin).rstrip("/")
        for origin in get_settings().runtime.backend_cors_origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Guards against HTTP Host Header attacks
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=get_settings().runtime.allowed_hosts,
)
