import { useState } from "react";
import { Link } from "react-router-dom";
import {
  FileText,
  Mail,
  Radar,
  ShieldCheck,
  Sparkles,
  TrendingUp,
} from "lucide-react";

import { runAgent } from "../../lib/api";

const agentCards = [
  {
    to: "/researcher",
    name: "Prospect Researcher",
    desc: "Turn any company into a decision-grade briefing — ARR, ICP fit, funding, signals, opener.",
    icon: Radar,
  },
  {
    to: "/hygiene",
    name: "CRM Hygiene Watchdog",
    desc: "Scan HubSpot for stale deals, missing fields, and data debt. A health score, not a lecture.",
    icon: ShieldCheck,
  },
  {
    to: "/sales",
    name: "Deal Intelligence",
    desc: "Read an active deal: stakeholders, buyer readiness, risk flags, next actions.",
    icon: TrendingUp,
  },
  {
    to: "/content",
    name: "Content Studio",
    desc: "Raw observation to a QC-scored draft. Your voice, your approval, nothing published without it.",
    icon: Sparkles,
  },
  {
    to: "/briefing",
    name: "Weekly Briefing",
    desc: "The Chief of Staff memo: pipeline pulse, OKRs, flags, and the one thing that matters.",
    icon: FileText,
  },
  {
    to: "/outbound",
    name: "Outbound Engine",
    desc: "Buying-intent signals into a three-step sequence. Evidence first, judgment always.",
    icon: Mail,
  },
];

export function HomeView() {
  const [status, setStatus] = useState("idle");
  const [output, setOutput] = useState(null);

  const run = async () => {
    setStatus("running");
    setOutput(null);
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
    <div className="max-w-4xl">
      <div className="mb-6 flex items-center gap-2 rounded bg-accent-500/10 border border-accent-500/30 px-4 py-3 text-sm text-accent-600">
        <Sparkles className="h-4 w-4" />
        <span>
          These agents are free to try on your own data. Part of the{" "}
          <a href="https://gtm-360.com" className="font-semibold underline hover:text-accent-700">
            GTM-360 advisory
          </a>{" "}
          service.
        </span>
      </div>

      <p className="text-xs font-bold text-accent-500 uppercase tracking-widest mb-3">
        GTM-360 Advisory
      </p>
      <h1 className="text-4xl font-bold text-primary leading-tight">
        Growth has slowed.
        <br />
        You're not sure why.
      </h1>
      <p className="mt-4 text-lg text-slate-500 max-w-2xl font-light leading-relaxed">
        This is the operator's desk. Six agents work the revenue system the way a senior operator
        would — they surface evidence, apply judgment, and wait for your call. No AI theater, no
        autonomous magic. Signals, evidence, decision support.
      </p>

      <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-5">
        {agentCards.map(({ to, name, desc, icon: Icon }) => (
          <Link
            key={to}
            to={to}
            className="card group p-6 hover:border-accent-500/40"
          >
            <div className="flex items-center gap-3">
              <Icon className="h-5 w-5 text-accent-500" />
              <h3 className="text-lg font-semibold text-primary group-hover:text-accent-600">
                {name}
              </h3>
            </div>
            <p className="mt-2 text-sm text-slate-500 leading-relaxed">{desc}</p>
          </Link>
        ))}
      </div>

      <div className="card mt-8 p-6">
        <h2 className="font-semibold text-primary">This week</h2>
        <p className="mt-1 text-sm text-slate-500">
          Run the weekly briefing to see where the revenue system stands. If the data hasn't been
          wired up yet, the agent will tell you plainly — that's the point.
        </p>
        <button
          onClick={run}
          disabled={status === "running"}
          className="btn btn-navy mt-4 disabled:opacity-50"
        >
          {status === "running" ? "Running…" : "Run weekly briefing"}
        </button>
        {output?.result && (
          <pre className="mt-4 max-h-96 overflow-auto rounded border border-slate-200 bg-slate-900 p-4 text-xs text-slate-200">
            {JSON.stringify(output.result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}