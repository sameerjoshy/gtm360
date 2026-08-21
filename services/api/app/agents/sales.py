"""Agent 3: Deal Intelligence / Sales Executor.

Analyzes an active deal: summary, stakeholders, buyer readiness,
risk flags, and next actions. Hardened from revenue-os sales_graph.
"""
from __future__ import annotations

from app.agents.base import BaseAgent
from app.core.hubspot import hubspot
from app.core.llm import llm

SYSTEM = """You are a sales execution analyst for a revenue-systems consultancy.
You read deal context and output buyer-readiness and risk assessment.
No fluff. Strict JSON."""

SCHEMA = """Return JSON:
{
  "summary": "...",
  "stakeholders": [{"name": "...", "role": "...", "influence": "CHAMPION|ECONOMIC|TECHNICAL|COACH|UNKNOWN"}],
  "buyer_readiness": 0.0,
  "risk_flags": [{"risk": "...", "severity": "LOW|MEDIUM|HIGH"}],
  "next_actions": ["..."]
}"""


class SalesAgent(BaseAgent):
    name = "sales"

    async def run(self, state):
        deal_id = str(state.get("deal_id") or "").strip()
        if not deal_id:
            state["status"] = "FAILED"
            state["error"] = "deal_id required"
            return state

        from app.core import demo

        if demo.is_demo(state):
            deals = demo.demo_deals()
        else:
            deals = await hubspot.search_deals(limit=200)

        deal = None
        for d in deals:
            if d.get("id") == deal_id:
                deal = d
                break

        if deal is None:
            state["status"] = "FAILED"
            state["error"] = f"deal not found: {deal_id}"
            return state

        props = deal.get("properties", {})
        try:
            analysis = llm.structured(
                f"""
DEAL: {props.get('dealname', deal_id)}
AMOUNT: {props.get('amount')}
STAGE: {props.get('dealstage')}
CLOSE DATE: {props.get('closedate')}
DAYS IN STAGE: {props.get('days_in_stage')}
LAST MODIFIED: {props.get('hs_lastmodifieddate')}
OWNER: {props.get('hubspot_owner_id')}

{SCHEMA}
""",
                SYSTEM,
            )
            analysis["deal_id"] = deal_id
            state["result"] = analysis
            state["status"] = "COMPLETED"
        except Exception as exc:
            state["status"] = "FAILED"
            state["error"] = str(exc)
        return state