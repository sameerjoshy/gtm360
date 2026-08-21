import { AgentShell } from "./AgentShell";

export function ContentView() {
  return (
    <AgentShell
      title="Content Studio"
      subtitle="Raw observation to a QC-scored, approval-gated post or email."
      agent="content"
      fields={[
        { key: "observation", label: "Raw observation", type: "textarea", placeholder: "What did you actually see or learn this week?" },
        { key: "format", label: "Format", placeholder: "tactical_scene | market_pov | lesson | email" },
      ]}
      buildBody={(i) => ({ observation: i.observation, format: i.format || "tactical_scene" })}
    />
  );
}