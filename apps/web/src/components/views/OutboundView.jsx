import { AgentShell } from "./AgentShell";

export function OutboundView() {
  return (
    <AgentShell
      title="Outbound Engine"
      subtitle="Detect buying-intent signals for a target account and draft a 3-step sequence."
      agent="outbound"
      fields={[{ key: "domain", label: "Target company domain", placeholder: "e.g. aligned.com" }]}
    />
  );
}