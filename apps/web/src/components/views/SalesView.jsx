import { AgentShell } from "./AgentShell";

export function SalesView() {
  return (
    <AgentShell
      title="Deal Intelligence"
      subtitle="Read an active deal the way a senior operator would: stakeholders, buyer readiness, risk flags, and the next action that moves it."
      agent="sales"
      fields={[{ key: "deal_id", label: "HubSpot deal ID", placeholder: "e.g. 20138472913" }]}
    />
  );
}