import { useState } from "react";

import { runAgent } from "../../lib/api";

export function AgentShell({ title, subtitle, agent, fields, buildBody, defaultInputs = {}, hint }) {
  const [inputs, setInputs] = useState(defaultInputs);
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
      <h1 className="text-3xl font-bold text-primary">{title}</h1>
      <p className="mt-2 text-slate-600">{subtitle}</p>

      <div className="card mt-8 p-6">
        <div className="space-y-4">
          {fields.map(({ key, label, placeholder, type = "text" }) => (
            <div key={key}>
              <label className="mb-1 block text-sm font-medium text-slate-700">{label}</label>
              {type === "textarea" ? (
                <textarea
                  value={inputs[key] || ""}
                  onChange={(e) => set(key, e.target.value)}
                  placeholder={placeholder}
                  rows={3}
                  className="w-full rounded border border-slate-300 bg-white px-3 py-2 text-sm focus:border-accent-500 focus:outline-none"
                />
              ) : (
                <input
                  value={inputs[key] || ""}
                  onChange={(e) => set(key, e.target.value)}
                  placeholder={placeholder}
                  className="w-full rounded border border-slate-300 bg-white px-3 py-2 text-sm focus:border-accent-500 focus:outline-none"
                />
              )}
            </div>
          ))}
        </div>

        <button
          onClick={run}
          disabled={status === "running"}
          className="btn btn-accent mt-5 disabled:opacity-50"
        >
          {status === "running" ? "Running…" : "Run"}
        </button>

        {hint && <p className="mt-3 text-xs text-slate-400">{hint}</p>}

        {status === "error" && (
          <div className="mt-4 rounded border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            {output?.error || "The agent could not complete this run."}
          </div>
        )}

        {output?.result && (
          <pre className="mt-5 max-h-96 overflow-auto rounded border border-slate-200 bg-slate-900 p-4 text-xs text-slate-200">
            {JSON.stringify(output.result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}