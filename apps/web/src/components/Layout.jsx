import {
  BriefcaseMedical,
  FileText,
  LayoutDashboard,
  Mail,
  Radar,
  ShieldCheck,
  Sparkles,
  TrendingUp,
} from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

const nav = [
  { to: "/", label: "Command Center", icon: LayoutDashboard, end: true },
  { to: "/researcher", label: "Prospect Researcher", icon: Radar },
  { to: "/hygiene", label: "CRM Hygiene", icon: ShieldCheck },
  { to: "/sales", label: "Deal Intelligence", icon: TrendingUp },
  { to: "/content", label: "Content Studio", icon: Sparkles },
  { to: "/briefing", label: "Weekly Briefing", icon: FileText },
  { to: "/outbound", label: "Outbound", icon: Mail },
];

export function Layout() {
  return (
    <div className="flex min-h-screen bg-secondary">
      <aside className="w-60 shrink-0 bg-primary text-white p-4">
        <div className="mb-6 flex items-center gap-2">
          <BriefcaseMedical className="h-6 w-6 text-accent-400" />
          <span className="text-lg font-bold tracking-tight">GTM-360</span>
        </div>
        <nav className="space-y-1">
          {nav.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded px-3 py-2 text-sm font-medium transition ${
                  isActive
                    ? "bg-accent-500 text-white"
                    : "text-slate-300 hover:bg-primary/40 hover:text-white"
                }`
              }
            >
              <Icon className="h-4 w-4" />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="mt-10 border-t border-white/10 pt-4 text-xs text-slate-400">
          <p>Revenue advisory, not AI theater.</p>
          <p className="mt-1">Every signal. Every judgment. Operator-grade.</p>
        </div>
      </aside>
      <main className="flex-1 p-8">
        <Outlet />
      </main>
    </div>
  );
}