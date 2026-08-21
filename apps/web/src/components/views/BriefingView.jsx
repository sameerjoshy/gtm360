import { AgentShell } from "./AgentShell";

export function BriefingView() {
  return (
    <AgentShell
      title="Weekly Exec Briefing"
      subtitle="Chief of Staff memo from live Supabase data: pipeline pulse, OKRs, escalations, one thing."
      agent="briefing"
      fields={[]}
      buildBody={() => ({})}
    />
  );
}