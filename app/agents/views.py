from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.models import Agent
from app.agents.schemas import AgentCreateRequest, AgentResponse
from app.core.database_session import new_async_session
from app.crypto.service import create_agent_identity

router = APIRouter()


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    payload: AgentCreateRequest,
    session: AsyncSession = Depends(new_async_session),
) -> AgentResponse:
    identity = create_agent_identity()
    agent = Agent(
        did=identity.did,
        name=payload.name,
        operator=payload.operator,
        public_key=identity.public_key_bytes,
        private_key_encrypted=identity.private_key_encrypted,
        metadata_json=payload.metadata,
    )
    session.add(agent)
    await session.commit()
    await session.refresh(agent)
    return AgentResponse.model_validate(_to_response_payload(agent))


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    session: AsyncSession = Depends(new_async_session),
) -> AgentResponse:
    agent = await session.scalar(select(Agent).where(Agent.id == agent_id))
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="agent_not_found",
        )
    return AgentResponse.model_validate(_to_response_payload(agent))


def _to_response_payload(agent: Agent) -> dict[str, object]:
    return {
        "id": agent.id,
        "did": agent.did,
        "name": agent.name,
        "operator": agent.operator,
        "metadata_json": agent.metadata_json,
        "created_at": agent.created_at,
        "status": "revoked" if agent.revoked_at else "active",
    }
