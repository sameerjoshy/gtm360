from typing import Any

from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    workspace_id: str
    run_id: str
    status: str
    error: str | None
    result: dict


class BaseAgent:
    """Convention all GTM360 agents follow.

    - One graph, one entry node (`run`)
    - `run` validates + normalizes inputs into state
    - Terminal state.status is COMPLETED / FAILED
    - result dict is the canonical output persisted to agent_runs
    """

    name: str = "base"

    def build(self) -> StateGraph:
        graph = StateGraph(AgentState)
        graph.add_node("run", self.run)
        graph.add_edge("run", END)
        return graph.compile()

    async def run(self, state: AgentState) -> AgentState:
        raise NotImplementedError

    def persist(self, state: AgentState) -> None:
        from app.core.supabase import supabase_client

        if state.get("run_id"):
            supabase_client.finish_agent_run(
                state["run_id"], state.get("result", {}), state.get("status", "COMPLETED")
            )

    async def execute(self, **kwargs: Any) -> dict:
        graph = self.build()
        state = await graph.ainvoke(kwargs)
        return state.get("result", {})