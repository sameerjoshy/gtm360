"""Agent 4: Content / CMO Agent.

Raw observation -> drafted post or email with a QC score and
approval gate. Inherits gtmbrain's content_queue flow.
"""
from __future__ import annotations

from app.agents.base import BaseAgent
from app.core.llm import llm

FORMATS = {
    "tactical_scene": "Bennett-style tactical scene from a live moment",
    "market_pov": "Gerhardt-style market point of view",
    "lesson": "Campbell/Welsh-style lesson from experience",
    "email": "short founder-sales cold email",
}

SYSTEM = """You are the CMO agent for GTM-360 (a revenue-systems consultancy).
Brand voice: Professional. Irreverent. Operator-driven. Three words.
Ground everything in the real observation. Short sentences. First person.
Score your own draft honestly — flag its weakness too."""

SCHEMA = """Return JSON:
{
  "format": "tactical_scene|market_pov|lesson|email",
  "channel": "linkedin|email",
  "draft": "...",
  "subject_line": "...",
  "qc_score": 0.0,
  "qc_notes": "...",
  "flag": {"weakness": "...", "recommendation": "..."}
}"""


class ContentAgent(BaseAgent):
    name = "content"

    async def run(self, state):
        observation = str(state.get("observation") or "").strip()
        fmt = str(state.get("format") or "tactical_scene").strip().lower()
        if not observation:
            state["status"] = "FAILED"
            state["error"] = "observation required"
            return state
        if fmt not in FORMATS:
            state["status"] = "FAILED"
            state["error"] = f"unknown format: {fmt}"
            return state

        try:
            draft = llm.structured(
                f"""
FORMAT: {FORMATS[fmt]}
RAW OBSERVATION: {observation}

{SCHEMA}
""",
                SYSTEM,
            )
            draft["format"] = fmt
            draft["approved"] = False
            draft["observation"] = observation

            try:
                from app.core.supabase import supabase_client

                supabase_client.upsert(
                    "content_queue",
                    [
                        {
                            "workspace_id": state.get("workspace_id", "default"),
                            "raw_observation": observation,
                            "post_format": fmt,
                            "draft": draft["draft"],
                            "qc_score": draft["qc_score"],
                            "qc_notes": draft["qc_notes"],
                            "status": "AWAITING_APPROVAL",
                        }
                    ],
                )
            except Exception:
                pass

            state["result"] = draft
            state["status"] = "COMPLETED"
        except Exception as exc:
            state["status"] = "FAILED"
            state["error"] = str(exc)
        return state