"""End-to-end smoke test for the six agents using a fake LLM provider.

No external keys required. Verifies each agent graph runs and produces
a COMPLETED state with a result payload.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agents import AGENTS  # noqa: E402
from app.core import llm  # noqa: E402


class FakeProvider:
    ready = True

    def complete(self, prompt, system, temperature=0.3):
        return '{"status": "ok", "fake": true}'


async def test(agent_name: str, inputs: dict):
    agent = AGENTS[agent_name]
    graph = agent.build()
    state = await graph.ainvoke({"run_id": f"test-{agent_name}", **inputs})
    result = state.get("result", {})
    print(f"[{agent_name}] status={state.get('status')} keys={sorted(result)}")
    assert state.get("status") == "COMPLETED", f"{agent_name} failed: {state.get('error')}"
    return result


async def main():
    llm._providers = [FakeProvider()]

    # Patch HubSpot for the sales agent so no external keys are required.
    from app.core import hubspot as hubspot_instance

    async def fake_search_deals(limit=50):
        return [
            {
                "id": "12345",
                "properties": {
                    "dealname": "Acme FCRO",
                    "amount": "20000",
                    "dealstage": "appointmentscheduled",
                    "closedate": None,
                    "days_in_stage": "3",
                    "hs_lastmodifieddate": None,
                    "hubspot_owner_id": "1",
                },
            }
        ]

    hubspot_instance.search_deals = fake_search_deals

    await test("researcher", {"domain": "revvana.com"})
    await test("hygiene", {"limit": 3})
    await test("sales", {"deal_id": "12345"})
    await test("content", {"observation": "We lost a deal because the buyer ghosted after legal."})
    await test("briefing", {"workspace_id": "test"})
    await test("outbound", {"domain": "aligned.com"})
    print("ALL AGENTS PASS")


if __name__ == "__main__":
    asyncio.run(main())