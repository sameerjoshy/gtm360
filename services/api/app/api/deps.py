from app.schemas.models import (
    AgentRunResponse,
    ContentRequest,
    DealRequest,
    DomainRequest,
    HygieneRequest,
)


class AgentInputs:
    """Map validated request bodies -> per-agent input state."""

    DOMAIN = DomainRequest
    HYGIENE = HygieneRequest
    DEAL = DealRequest
    CONTENT = ContentRequest

    @staticmethod
    def domain(req: DomainRequest) -> dict:
        return {"domain": req.domain, "record_id": req.record_id}

    @staticmethod
    def hygiene(req: HygieneRequest) -> dict:
        return {"limit": req.limit, "company_limit": req.company_limit}

    @staticmethod
    def deal(req: DealRequest) -> dict:
        return {"deal_id": req.deal_id}

    @staticmethod
    def content(req: ContentRequest) -> dict:
        return {"observation": req.observation, "format": req.format}


def run_response(state: dict) -> AgentRunResponse:
    return AgentRunResponse(
        run_id=state.get("run_id", ""),
        status=state.get("status", "FAILED"),
        result=state.get("result"),
        error=state.get("error"),
    )