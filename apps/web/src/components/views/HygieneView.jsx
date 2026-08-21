import { AgentShell } from "./AgentShell";

export function HygieneView() {
  return (
    <AgentShell
      title="CRM Hygiene Watchdog"
      subtitle="Scan HubSpot for stale deals, missing fields, and data debt. Get a health score and fix actions."
      agent="hygiene"
      fields={[]}
      buildBody={() => ({ limit: 100, company_limit: 20 })}
    />
  );
}