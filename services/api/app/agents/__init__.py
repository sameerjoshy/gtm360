from app.agents.base import BaseAgent
from app.agents.briefing import BriefingAgent
from app.agents.content import ContentAgent
from app.agents.hygiene import HygieneAgent
from app.agents.outbound import OutboundAgent
from app.agents.researcher import ResearcherAgent
from app.agents.sales import SalesAgent

AGENTS: dict[str, BaseAgent] = {
    "researcher": ResearcherAgent(),
    "hygiene": HygieneAgent(),
    "sales": SalesAgent(),
    "content": ContentAgent(),
    "briefing": BriefingAgent(),
    "outbound": OutboundAgent(),
}

__all__ = ["AGENTS", "BaseAgent"]