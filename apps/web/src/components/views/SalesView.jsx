import { AgentShell } from "./AgentShell";

export function SalesView() {
  return (
    <AgentShell
      title="Deal Intelligence"
      subtitle="Analyze an active deal: stakeholders, buyer readiness, risk flags, next actions."
      agent="sales"
      fields={[{ key: "deal_id", label: "HubSpot deal ID", placeholder: "e.g. 20138472913" }]}
    />
  );
}