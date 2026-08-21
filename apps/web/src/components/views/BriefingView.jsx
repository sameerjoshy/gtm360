import { AgentShell } from "./AgentShell";

export function BriefingView() {
  return (
    <AgentShell
      title="Weekly Exec Briefing"
      subtitle="The Chief of Staff memo from live data: pipeline pulse, OKRs, escalations, flags, and the single most important thing."
      agent="briefing"
      fields={[]}
      buildBody={() => ({})}
    />
  );
}