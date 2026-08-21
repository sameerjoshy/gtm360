"""Agent 6: Outbound Engine (Signal360).

Detects buying intent signals for a target account and produces a
personalized, sequenced outreach draft. Consolidates OpenSignal's
signal-scoring + gtmbrain's proposal flows into one agent.
"""
from __future__ import annotations

import httpx

from app.agents.base import BaseAgent
from app.core.llm import llm

SIGNAL_RULES = [
    ("hiring_sales", "hiring", ["hiring", "careers", "jobs", "sales development"]),
    ("hiring_exec", "exec-hiring", ["chief revenue officer", "head of sales", "vp sales"]),
    ("funding", "funding", ["series a", "series b", "raised", "seed"]),
    ("expansion", "expansion", ["expanding", "new office", "growing team"]),
    ("replatforming", "replatform", ["migrating", "hubspot", "salesforce", "crm"]),
    ("laid_off", "layoff", ["layoff", "restructuring", "downsizing"]),
]

SYSTEM = """You are the outbound engineer for GTM-360.
You score buying intent from raw signals and write one personalized,
peer-to-peer cold email. Never sycophantic, never generic.
Output strict JSON."""

SCHEMA = """Return JSON:
{
  "intent_score": 0.0,
  "intent": "HIGH|MEDIUM|LOW",
  "matched_signals": [{"type": "...", "detail": "..."}],
  "sequence": [
    {"step": 1, "channel": "email", "subject": "...", "body": "...", "delay_days": 0},
    {"step": 2, "channel": "email", "subject": "...", "body": "...", "delay_days": 3},
    {"step": 3, "channel": "linkedin", "subject": "", "body": "...", "delay_days": 6}
  ],
  "rationale": "..."
}"""


class OutboundAgent(BaseAgent):
    name = "outbound"

    async def run(self, state):
        domain = str(state.get("domain") or "").strip().lower()
        if not domain:
            state["status"] = "FAILED"
            state["error"] = "domain required"
            return state

        raw_signals = await self._detect(domain)
        matched = self._score(raw_signals)
        intent_score = self._intent_score(matched)

        try:
            campaign = llm.structured(
                f"""
TARGET DOMAIN: {domain}
MATCHED SIGNALS: {matched}
INTENT SCORE: {intent_score}
SERVICE: GTM Diagnostic / Fractional CRO / RevOps Audit
BRAND: Professional. Irreverent. Operator-driven.

{SCHEMA}
""",
                SYSTEM,
            )
            campaign["intent_score"] = round(intent_score, 2)
            state["result"] = campaign
            state["status"] = "COMPLETED"
        except Exception as exc:
            state["status"] = "FAILED"
            state["error"] = str(exc)
        return state

    async def _detect(self, domain: str) -> list:
        """Scrape key pages for raw signal keywords. All free."""
        pages = [f"https://{domain}", f"https://{domain}/careers", f"https://{domain}/about"]
        hits = []
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
            for url in pages:
                try:
                    r = await c.get(url, headers={"User-Agent": "Mozilla/5.0"})
                    if r.status_code == 200:
                        text = " ".join(r.text.split()).lower()
                        for sig_type, label, keywords in SIGNAL_RULES:
                            for kw in keywords:
                                if kw in text:
                                    hits.append({"type": sig_type, "detail": f"{label}: found on {url}"})
                                    break
                except Exception:
                    continue
        return hits

    def _score(self, hits: list) -> list:
        seen = set()
        dedup = []
        for h in hits:
            if h["type"] not in seen:
                seen.add(h["type"])
                dedup.append(h)
        return dedup

    def _intent_score(self, matched: list) -> float:
        weights = {
            "hiring_sales": 0.9,
            "hiring_exec": 1.0,
            "funding": 0.7,
            "expansion": 0.6,
            "replatforming": 0.8,
            "laid_off": 0.4,
        }
        if not matched:
            return 0.0
        return min(1.0, sum(weights.get(m["type"], 0.5) for m in matched) / 3.0)