import { AgentShell } from "./AgentShell";

export function OutboundView() {
  return (
    <AgentShell
      title="Outbound Engine"
      subtitle="Buying-intent signals become a three-step sequence. Evidence first, judgment always — nothing goes out without your call."
      agent="outbound"
      fields={[{ key: "domain", label: "Target company domain", placeholder: "e.g. aligned.com" }]}
    />
  );
}