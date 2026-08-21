"""Agent 2: CRM Hygiene + Stale-Deal Watchdog.

Scans HubSpot deals + companies, flags stale deals / missing fields /
bad data, scores CRM health, and writes findings + fix suggestions
to Supabase.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.agents.base import BaseAgent
from app.core.hubspot import hubspot
from app.core.llm import llm

STALE_DAYS = 14
WATCHED_FIELDS = [
    "amount",
    "closedate",
    "hubspot_owner_id",
    "days_in_stage",
]


class HygieneAgent(BaseAgent):
    name = "hygiene"

    async def run(self, state):
        from app.core import demo

        if demo.is_demo(state):
            deals = demo.demo_deals()
            companies = [
                demo.demo_company(d["properties"].get("associatedcompanyid"))
                for d in deals
                if demo.demo_company(d["properties"].get("associatedcompanyid"))
            ]
        else:
            deals = await hubspot.search_deals(limit=state.get("limit", 100))
            companies = []
            for deal in deals[: int(state.get("company_limit", 20))]:
                try:
                    cid = deal["properties"].get("associatedcompanyid")
                    if cid:
                        companies.append(await hubspot.read_company(cid))
                except Exception:
                    continue

        now = datetime.now(timezone.utc)
        issues = []
        for deal in deals:
            props = deal.get("properties", {})
            name = props.get("dealname", deal.get("id"))
            for field in WATCHED_FIELDS:
                if not props.get(field) or props.get(field) in ("", "0"):
                    issues.append(
                        {
                            "severity": "HIGH",
                            "object": "deal",
                            "object_id": deal.get("id"),
                            "name": name,
                            "issue": f"missing field: {field}",
                        }
                    )
            last = props.get("hs_lastmodifieddate")
            if last:
                try:
                    modified = datetime.fromisoformat(last.replace("Z", "+00:00"))
                    if now - modified > timedelta(days=STALE_DAYS):
                        issues.append(
                            {
                                "severity": "MEDIUM",
                                "object": "deal",
                                "object_id": deal.get("id"),
                                "name": name,
                                "issue": f"stale: no activity for {STALE_DAYS}+ days",
                            }
                        )
                except ValueError:
                    pass

        suggestions = await self._suggest(issues, deals)
        health = self._health_score(len(deals), issues)

        result = {
            "scanned": {"deals": len(deals), "companies": len(companies)},
            "health_score": health,
            "issue_count": len(issues),
            "issues": issues[:50],
            "suggestions": suggestions,
        }

        try:
            from app.core.supabase import supabase_client

            supabase_client.upsert(
                "hygiene_scans",
                [
                    {
                        "workspace_id": state.get("workspace_id", "default"),
                        "health_score": health,
                        "issue_count": len(issues),
                        "issues": result["issues"],
                        "scanned_at": now.isoformat(),
                    }
                ],
            )
        except Exception:
            pass

        state["result"] = result
        state["status"] = "COMPLETED"
        return state

    def _health_score(self, total: int, issues: list) -> float:
        if total == 0:
            return 0.0
        missing = sum(1 for i in issues if i["severity"] == "HIGH")
        stale = sum(1 for i in issues if i["severity"] == "MEDIUM")
        return round(max(0.0, 100 - (missing * 4) - (stale * 1.5)) / 100, 2)

    async def _suggest(self, issues: list, deals: list) -> list:
        if not issues:
            return []
        try:
            return llm.structured(
                f"""Given these CRM issues, propose concrete fix actions (JSON array
of {{"issue": "...", "action": "...", "owner": "..."}}).

Issues:
{issues}

Deals scanned: {len(deals)}""",
                "You return strict JSON only. Practical, ops-grade fixes.",
            )
        except Exception:
            return [{"issue": i["issue"], "action": "review in HubSpot", "owner": "unassigned"} for i in issues[:5]]