import uuid

from fastapi import APIRouter, HTTPException

from app.agents import AGENTS
from app.api.deps import AgentInputs, run_response
from app.core.supabase import supabase_client
from app.schemas.models import (
    AgentRunResponse,
    ContentRequest,
    DealRequest,
    DomainRequest,
    HygieneRequest,
)

router = APIRouter(prefix="/api/v1", tags=["agents"])


@router.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0", "agents": sorted(AGENTS)}


@router.post("/agents/{agent_name}/run", response_model=AgentRunResponse)
async def run_agent(agent_name: str, body: dict):
    if agent_name not in AGENTS:
        raise HTTPException(status_code=404, detail=f"unknown agent: {agent_name}")

    agent = AGENTS[agent_name]
    inputs = dict(body)

    try:
        run_id = supabase_client.create_agent_run(agent_name, inputs)
    except Exception:
        run_id = str(uuid.uuid4())

    state = {"run_id": run_id, **inputs}
    try:
        graph = agent.build()
        final = await graph.ainvoke(state)
        if final.get("run_id"):
            agent.persist(final)
        return run_response(final)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/researcher", response_model=AgentRunResponse)
async def researcher(req: DomainRequest):
    return await run_agent("researcher", AgentInputs.domain(req))


@router.post("/hygiene/scan", response_model=AgentRunResponse)
async def hygiene_scan(req: HygieneRequest):
    return await run_agent("hygiene", AgentInputs.hygiene(req))


@router.post("/sales/analyze", response_model=AgentRunResponse)
async def sales_analyze(req: DealRequest):
    return await run_agent("sales", AgentInputs.deal(req))


@router.post("/content/draft", response_model=AgentRunResponse)
async def content_draft(req: ContentRequest):
    return await run_agent("content", AgentInputs.content(req))


@router.post("/briefing/weekly", response_model=AgentRunResponse)
async def weekly_briefing():
    return await run_agent("briefing", {"workspace_id": "default"})


@router.post("/outbound/campaign", response_model=AgentRunResponse)
async def outbound_campaign(req: DomainRequest):
    return await run_agent("outbound", AgentInputs.domain(req))