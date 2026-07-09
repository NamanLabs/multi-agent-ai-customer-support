import { CreditCard, Wrench, Package, AlertTriangle, HelpCircle, TriangleAlert, CheckCircle2 } from "lucide-react";
import { useState, useEffect } from "react";

const AGENT_META = {
  "Billing Agent": { icon: CreditCard, color: "#3D5A82", bg: "#EAF0F8" },
  "Technical Support Agent": { icon: Wrench, color: "#008C80", bg: "#E4F8F5" },
  "Product Agent": { icon: Package, color: "#6D4FA8", bg: "#F1ECFA" },
  "Complaint Agent": { icon: AlertTriangle, color: "#B5760C", bg: "#FDF2E0" },
  "FAQ Agent": { icon: HelpCircle, color: "#5B6270", bg: "#EEEFF1" },
};

function metaFor(agent) {
  return AGENT_META[agent] || { icon: HelpCircle, color: "#5B6270", bg: "#EEEFF1" };
}

/**
 * Routing Receipt: the signature visual element of this interface.
 * Shows exactly which specialized agent(s) handled the query, a live
 * confidence bar, and escalation state -- making the multi-agent
 * architecture visible instead of hiding it behind a plain chat bubble.
 */
export default function RoutingReceipt({ agentsInvoked, confidence, escalated }) {
  const confidencePct = Math.round((confidence || 0) * 100);
  const barColor = escalated ? "#F5A623" : confidencePct < 60 ? "#F5A623" : "#00B8A9";

  // Animate the confidence bar filling from 0 -> actual value on mount
  const [barWidth, setBarWidth] = useState(0);
  useEffect(() => {
    const id = requestAnimationFrame(() => setBarWidth(confidencePct));
    return () => cancelAnimationFrame(id);
  }, [confidencePct]);

  return (
    <div className="stamp-in mt-2 max-w-xs">
      <div className="rounded-xl border border-gray-200 dark:border-white/10 bg-white dark:bg-card-dark shadow-soft overflow-hidden">
        <div className="flex items-center gap-1.5 px-3 py-2 border-b border-gray-100 dark:border-white/10 flex-wrap">
          {agentsInvoked.map((agent) => {
            const meta = metaFor(agent);
            const Icon = meta.icon;
            return (
              <span
                key={agent}
                className="flex items-center gap-1 pl-1.5 pr-2 py-1 rounded-full dark:opacity-90"
                style={{ backgroundColor: meta.bg }}
              >
                <Icon size={11} style={{ color: meta.color }} />
                <span className="text-[10.5px] font-medium" style={{ color: meta.color }}>
                  {agent.replace(" Agent", "").replace(" Support", "")}
                </span>
              </span>
            );
          })}
        </div>

        <div className="px-3 py-2">
          <div className="flex items-center justify-between mb-1">
            <span className="text-[10px] uppercase tracking-wide text-muted dark:text-muted-dark font-mono">
              routing confidence
            </span>
            <span className="text-[11px] font-mono font-medium" style={{ color: barColor }}>
              {confidencePct}%
            </span>
          </div>
          <div className="h-1.5 rounded-full bg-gray-100 dark:bg-white/10 overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-700 ease-out"
              style={{ width: `${barWidth}%`, backgroundColor: barColor }}
            />
          </div>
        </div>

        <div
          className={`flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-medium ${
            escalated
              ? "bg-amber/10 dark:bg-amber/15 text-amber-700 dark:text-amber-300"
              : "bg-teal/10 dark:bg-teal/15 text-teal-dark dark:text-teal-light"
          }`}
        >
          {escalated ? <TriangleAlert size={12} /> : <CheckCircle2 size={12} />}
          {escalated ? "Flagged for human review" : "Auto-resolved"}
        </div>
      </div>
    </div>
  );
}
