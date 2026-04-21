from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AgentCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    operator: str | None = Field(default=None, max_length=320)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    did: str
    name: str
    operator: str | None
    metadata: dict[str, Any] = Field(
        validation_alias="metadata_json",
        serialization_alias="metadata",
    )
    created_at: datetime
    status: str
