import { AgentShell } from "./AgentShell";

export function ResearcherView() {
  return (
    <AgentShell
      title="Prospect Researcher"
      subtitle="Turn any company into a decision-grade briefing: ARR, funding, ICP fit, signals, opener."
      agent="researcher"
      fields={[{ key: "domain", label: "Company domain", placeholder: "e.g. revvana.com" }]}
    />
  );
}