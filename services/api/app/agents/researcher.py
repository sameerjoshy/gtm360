"""Agent 1: Prospect Researcher.

Company/domain -> briefing: ARR, funding, growth signals, ICP fit, opener.
Inherited and hardened from gtm360-revenue-os researcher_graph.
"""
from __future__ import annotations

import httpx

from app.agents.base import BaseAgent
from app.core.llm import llm

SYSTEM = """You are a senior GTM researcher at a revenue-systems consultancy.
You turn raw company facts into a tight, decision-grade prospect briefing.
Professional, irreverent, operator-driven. Never sycophantic.
Output strict JSON."""

SCHEMA_INSTRUCTIONS = """Return JSON with exactly these keys:
{
  "domain": "...",
  "company": "...",
  "location": "...",
  "headcount": int or null,
  "arr_estimate_usd": int or null,
  "funding": {"status": "...", "total_usd": int or null, "latest_round": "...", "latest_date": "...", "investors": [...]},
  "signals": [{"type": "...", "detail": "..."}],
  "icp_score": 0.0,
  "icp_fit": "STRONG|MODERATE|WEAK|UNKNOWN",
  "openers": [{"hook_type": "...", "text": "..."}],
  "summary": "..."
}"""


class ResearcherAgent(BaseAgent):
    name = "researcher"

    async def run(self, state):
        domain = str(state.get("domain") or "").strip().lower()
        if not domain:
            state["status"] = "FAILED"
            state["error"] = "domain required"
            return state

        facts = await self._gather(domain)
        prompt = self._build_prompt(domain, facts)
        try:
            briefing = llm.structured(prompt, SYSTEM)
            briefing["domain"] = domain
            briefing.setdefault("signals", [])
            state["result"] = {"briefing": briefing, "sources": facts.get("sources", [])}
            state["status"] = "COMPLETED"
        except Exception as exc:
            state["status"] = "FAILED"
            state["error"] = str(exc)
        return state

    async def _gather(self, domain: str) -> dict:
        """Free-tier research: website scrape + structured web search endpoints."""
        sources = []
        payload = {}

        # 1. Try the website homepage (strips tracking).
        try:
            async with httpx.AsyncClient(timeout=20, follow_redirects=True) as c:
                resp = await c.get(f"https://{domain}", headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code == 200:
                    text = " ".join(resp.text.split())[:12000]
                    payload["website_text"] = text
                    sources.append(f"https://{domain}")
        except Exception:
            payload["website_text"] = None

        # 2. Optional structured signal enrichment via llm-proxy worker.
        from app.core.config import settings

        proxy = getattr(settings, "llm_proxy_url", None)
        if proxy:
            try:
                async with httpx.AsyncClient(timeout=20) as c:
                    r = await c.post(proxy, json={"query": f"{domain} funding ARR employees"})
                    if r.status_code == 200:
                        payload["web_signals"] = r.json()
                        sources.append(proxy)
            except Exception:
                pass

        return {"payload": payload, "sources": sources}

    def _build_prompt(self, domain: str, facts: dict) -> str:
        payload = facts.get("payload", {})
        text = payload.get("website_text")
        signals = payload.get("web_signals")
        return f"""
Researcher briefing for {domain}.

WEBSITE CONTENT:
{text if text else "(could not fetch)"}

WEB SIGNALS:
{signals if signals else "(none)"}

{SCHEMA_INSTRUCTIONS}
"""