from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.audit.models import VerificationLog
from app.audit.schemas import VerificationLogResponse
from app.core.database_session import new_async_session

router = APIRouter()


@router.get("", response_model=list[VerificationLogResponse])
async def list_audit_logs(
    agent_id: str | None = None,
    result: str | None = None,
    from_: datetime | None = Query(default=None, alias="from"),
    to: datetime | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    session: AsyncSession = Depends(new_async_session),
) -> list[VerificationLog]:
    query = select(VerificationLog)
    if agent_id is not None:
        query = query.where(VerificationLog.agent_did == agent_id)
    if result is not None:
        query = query.where(VerificationLog.result == result)
    if from_ is not None:
        query = query.where(VerificationLog.verified_at >= from_)
    if to is not None:
        query = query.where(VerificationLog.verified_at <= to)

    query = query.order_by(VerificationLog.verified_at.desc()).limit(limit)
    return list(await session.scalars(query))
