import { AgentShell } from "./AgentShell";

export function ResearcherView() {
  return (
    <AgentShell
      title="Prospect Researcher"
      subtitle="Turn any company into a decision-grade briefing: ARR, funding, ICP fit, signals, and the opener that actually works."
      agent="researcher"
      fields={[{ key: "domain", label: "Company domain", placeholder: "e.g. revvana.com" }]}
    />
  );
}