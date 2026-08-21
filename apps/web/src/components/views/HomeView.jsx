import { useState } from "react";

import { runAgent } from "../../lib/api";

export function HomeView() {
  const [status, setStatus] = useState("idle");
  const [output, setOutput] = useState(null);

  const run = async () => {
    setStatus("running");
    try {
      const res = await runAgent("briefing", {});
      setOutput(res);
      setStatus(res.status === "COMPLETED" ? "done" : "error");
    } catch (e) {
      setStatus("error");
      setOutput({ error: e.message });
    }
  };

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold">Command Center</h1>
      <p className="mt-1 text-slate-400">
        One cockpit for six agents. No overlap — every view hits the unified API.
      </p>

      <div className="mt-6 rounded-xl border border-ink-700 bg-ink-800 p-6">
        <h2 className="font-semibold">This week</h2>
        <p className="mt-2 text-sm text-slate-400">
          Run the weekly Chief-of-Staff briefing to see pipeline pulse, OKRs, flags, and the
          single most important thing.
        </p>
        <button
          onClick={run}
          disabled={status === "running"}
          className="mt-4 rounded-lg bg-accent-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-accent-400 disabled:opacity-50"
        >
          {status === "running" ? "Running…" : "Run weekly briefing"}
        </button>
        {output && (
          <pre className="mt-4 max-h-96 overflow-auto rounded-lg bg-ink-900 p-4 text-xs text-slate-300">
            {JSON.stringify(output, null, 2)}
          </pre>
        )}
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4">
        {["researcher", "hygiene", "sales", "content", "briefing", "outbound"].map((a) => (
          <div key={a} className="rounded-xl border border-ink-700 bg-ink-800 p-4">
            <div className="font-medium capitalize">{a}</div>
            <div className="mt-1 text-xs text-slate-400">Agent ready</div>
          </div>
        ))}
      </div>
    </div>
  );
}