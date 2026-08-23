"""Agent 5: Weekly Exec Briefing (Chief of Staff).

Reads pipeline snapshot, OKR tracker, escalations from Supabase and
synthesizes a Smart-Brevity weekly memo with a single "one thing".
"""
from __future__ import annotations

from datetime import datetime, timezone

from app.agents.base import BaseAgent
from app.core.llm import llm

SYSTEM = """You are the Chief of Staff for a one-person GTM consultancy.
You synthesize messy operational data into a Smart-Brevity weekly memo.
Warm, direct, pushes back, never sycophantic.
Output strict JSON."""

SCHEMA = """Return JSON:
{
  "week": "...",
  "pipeline_pulse": {"total_value_usd": 0, "deal_count": 0, "live_stages": 0, "proposals_sent": 0},
  "okr_status": [{"objective": "...", "krs": [{"kr": "...", "current": 0, "target": 0}]}],
  "plan_link": "okr.gtm-360.com",
  "escalations": [{"summary": "..."}],
  "flags": [{"severity": "LOW|MEDIUM|HIGH", "flag": "..."}],
  "one_thing": "...",
  "priorities": ["..."]
}"""


class BriefingAgent(BaseAgent):
    name = "briefing"

    async def run(self, state):
        workspace = state.get("workspace_id", "default")

        from app.core import demo

        if demo.is_demo(state):
            rows = demo.DEMO_PIPELINE
            esc_rows = demo.DEMO_ESCALATIONS
            okr_payload = []
            for o in demo.DEMO_OKRS:
                krs = [
                    {"kr": kr["kr_text"], "current": kr["current"], "target": kr["target"]}
                    for kr in o["krs"]
                ]
                okr_payload.append({"objective": o["objective_text"], "krs": krs})
        else:
            try:
                from app.core.supabase import supabase_client

                pipeline = supabase_client.table("pipeline_snapshot").select("*").execute()
                okrs = supabase_client.table("okr_tracker").select("*").execute()
                escalations = supabase_client.table("escalations").select("*").execute()
                rows = pipeline.data or []
                okr_rows = okrs.data or []
                esc_rows = escalations.data or []
                okr_payload = []
                for o in okr_rows:
                    krs = [
                        {
                            "kr": o.get("kr_text"),
                            "current": o.get("kr_current"),
                            "target": o.get("kr_target"),
                        }
                    ]
                    okr_payload.append({"objective": o.get("objective_text"), "krs": krs})
            except Exception:
                # Graceful fallback when Supabase schema isn't provisioned yet.
                rows, okr_rows, esc_rows = [], [], []
                okr_payload = []

        total = sum(float(r.get("amount") or 0) for r in rows)
        live = [r for r in rows if r.get("stage") not in ("closedwon", "closedlost")]

        raw = {
            "week_ending": datetime.now(timezone.utc).date().isoformat(),
            "pipeline_total_usd": round(total),
            "live_deals": len(live),
            "proposals_sent": sum(1 for r in rows if r.get("stage") == "proposal"),
            "okrs": okr_payload,
            "escalation_count": len(esc_rows),
            "data_source": "demo workspace" if demo.is_demo(state) else ("supabase" if rows else "empty (no data provisioned)"),
        }

        try:
            memo = llm.structured(
                f"""
OPERATIONAL DATA (JSON):
{raw}

{SCHEMA}
""",
                SYSTEM,
            )
            # OKRs are planned in Plan (okr.gtm-360.com); this snapshot is read-only reference.
            memo["plan_link"] = "okr.gtm-360.com"
            memo.setdefault("okr_status", okr_payload)
            pulse = memo.setdefault("pipeline_pulse", {})
            pulse["total_value_usd"] = round(total)
            pulse["deal_count"] = len(rows)
            pulse["live_stages"] = len(live)
            memo["pipeline_pulse"] = pulse
            state["result"] = memo
            state["status"] = "COMPLETED"
        except Exception as exc:
            state["status"] = "FAILED"
            state["error"] = str(exc)
        return state