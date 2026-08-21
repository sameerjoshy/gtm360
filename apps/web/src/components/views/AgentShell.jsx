import { useState } from "react";

import { runAgent } from "../../lib/api";

export function AgentShell({ title, subtitle, agent, fields, buildBody }) {
  const [inputs, setInputs] = useState({});
  const [status, setStatus] = useState("idle");
  const [output, setOutput] = useState(null);

  const set = (k, v) => setInputs((s) => ({ ...s, [k]: v }));

  const run = async () => {
    setStatus("running");
    setOutput(null);
    try {
      const res = await runAgent(agent, buildBody ? buildBody(inputs) : inputs);
      setOutput(res);
      setStatus(res.status === "COMPLETED" ? "done" : "error");
    } catch (e) {
      setStatus("error");
      setOutput({ error: e.message });
    }
  };

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold">{title}</h1>
      <p className="mt-1 text-slate-400">{subtitle}</p>

      <div className="mt-6 rounded-xl border border-ink-700 bg-ink-800 p-6">
        <div className="space-y-3">
          {fields.map(({ key, label, placeholder, type = "text" }) => (
            <div key={key}>
              <label className="mb-1 block text-sm font-medium text-slate-300">{label}</label>
              {type === "textarea" ? (
                <textarea
                  value={inputs[key] || ""}
                  onChange={(e) => set(key, e.target.value)}
                  placeholder={placeholder}
                  rows={3}
                  className="w-full rounded-lg border border-ink-700 bg-ink-900 px-3 py-2 text-sm focus:border-accent-500 focus:outline-none"
                />
              ) : (
                <input
                  value={inputs[key] || ""}
                  onChange={(e) => set(key, e.target.value)}
                  placeholder={placeholder}
                  className="w-full rounded-lg border border-ink-700 bg-ink-900 px-3 py-2 text-sm focus:border-accent-500 focus:outline-none"
                />
              )}
            </div>
          ))}
        </div>

        <button
          onClick={run}
          disabled={status === "running"}
          className="mt-4 rounded-lg bg-accent-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-accent-400 disabled:opacity-50"
        >
          {status === "running" ? "Running…" : "Run agent"}
        </button>

        {status === "error" && (
          <div className="mt-4 rounded-lg border border-red-700 bg-red-950/40 p-4 text-sm text-red-200">
            {output?.error || "Agent failed"}
          </div>
        )}

        {output?.result && (
          <pre className="mt-4 max-h-96 overflow-auto rounded-lg bg-ink-900 p-4 text-xs text-slate-300">
            {JSON.stringify(output.result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}