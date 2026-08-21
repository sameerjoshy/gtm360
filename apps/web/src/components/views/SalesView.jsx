import { AgentShell } from "./AgentShell";

export function SalesView() {
  return (
    <AgentShell
      title="Deal Intelligence"
      subtitle="Read a deal the way a senior operator would: stakeholders, buyer readiness, risk flags, and the next action that moves it."
      agent="sales"
      fields={[{ key: "deal_id", label: "Deal ID", placeholder: "e.g. demo-1001 (sample) or your HubSpot deal ID" }]}
      defaultInputs={{ deal_id: "demo-1001" }}
      hint="Try demo-1001, demo-1002, or demo-1007 from the sample workspace."
    />
  );
}