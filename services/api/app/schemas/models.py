from pydantic import BaseModel, Field


class DomainRequest(BaseModel):
    domain: str = Field(..., min_length=2)
    record_id: str | None = None


class HygieneRequest(BaseModel):
    limit: int = 100
    company_limit: int = 20


class DealRequest(BaseModel):
    deal_id: str = Field(..., min_length=1)


class ContentRequest(BaseModel):
    observation: str = Field(..., min_length=5)
    format: str = "tactical_scene"


class AgentRunResponse(BaseModel):
    run_id: str
    status: str
    result: dict | None = None
    error: str | None = None