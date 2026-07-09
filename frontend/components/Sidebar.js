import {
  Search, Plus, CreditCard, Wrench, Package, AlertTriangle, HelpCircle,
  PanelLeftClose, PanelLeftOpen, Trash2, Sun, Moon,
} from "lucide-react";
import { useState } from "react";

const AGENT_META = {
  Billing: { icon: CreditCard, color: "#7FA8D4" },
  Technical: { icon: Wrench, color: "#3DD4C6" },
  Product: { icon: Package, color: "#B79CE8" },
  Complaint: { icon: AlertTriangle, color: "#FFC15C" },
  FAQ: { icon: HelpCircle, color: "#A8ACB3" },
};

export default function Sidebar({
  sessions, activeSessionId, onSelectSession, onNewChat, onDeleteSession,
  collapsed, onToggleCollapsed, theme, onToggleTheme,
}) {
  const [query, setQuery] = useState("");
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);
  const [themeIconFlip, setThemeIconFlip] = useState(false);

  const filtered = sessions.filter((s) =>
    (s.preview || "").toLowerCase().includes(query.toLowerCase())
  );

  function handleDeleteClick(e, id) {
    e.stopPropagation();
    if (confirmDeleteId === id) {
      onDeleteSession(id);
      setConfirmDeleteId(null);
    } else {
      setConfirmDeleteId(id);
    }
  }

  function handleThemeToggle() {
    setThemeIconFlip(true);
    onToggleTheme();
    setTimeout(() => setThemeIconFlip(false), 400);
  }

  const ThemeIcon = theme === "light" ? Sun : Moon;

  return (
    <aside
      className={`bg-navy-gradient text-white flex flex-col h-full shrink-0 relative overflow-hidden transition-[width] duration-300 ease-in-out ${
        collapsed ? "w-16" : "w-72"
      }`}
    >
      {/* Collapsed rail content */}
      <div
        className={`absolute inset-0 flex flex-col items-center py-6 gap-4 transition-opacity duration-200 ${
          collapsed ? "opacity-100 delay-150" : "opacity-0 pointer-events-none"
        }`}
      >
        <button
          onClick={onToggleCollapsed}
          className="w-9 h-9 rounded-lg flex items-center justify-center hover:bg-white/10 transition-colors"
          aria-label="Expand sidebar"
        >
          <PanelLeftOpen size={17} className="text-white/70" />
        </button>
        <button
          onClick={onNewChat}
          className="w-9 h-9 rounded-lg flex items-center justify-center bg-white/10 hover:bg-white/15 transition-colors"
          aria-label="New conversation"
        >
          <Plus size={16} />
        </button>
        <div className="flex-1 overflow-y-auto flex flex-col items-center gap-2 mt-2">
          {sessions.slice(0, 12).map((s) => {
            const meta = AGENT_META[s.lastAgent];
            return (
              <button
                key={s.id}
                onClick={() => onSelectSession(s.id)}
                title={s.preview}
                className="w-2 h-2 rounded-full shrink-0 transition-transform hover:scale-125"
                style={{
                  backgroundColor: meta ? meta.color : "rgba(255,255,255,0.25)",
                  outline: s.id === activeSessionId ? "2px solid rgba(255,255,255,0.5)" : "none",
                  outlineOffset: "2px",
                }}
              />
            );
          })}
        </div>
        <button
          onClick={handleThemeToggle}
          className="w-9 h-9 rounded-lg flex items-center justify-center hover:bg-white/10 transition-colors"
          aria-label="Toggle theme"
        >
          <ThemeIcon size={15} className={`text-white/60 ${themeIconFlip ? "icon-flip" : ""}`} />
        </button>
      </div>

      {/* Expanded content */}
      <div
        className={`flex flex-col h-full transition-opacity duration-200 ${
          collapsed ? "opacity-0 pointer-events-none" : "opacity-100 delay-150"
        }`}
      >
        <div className="px-5 py-6 border-b border-white/10 flex items-center gap-3">
          <div className="min-w-0">
            <h1 className="font-display font-semibold text-[15px] tracking-tight leading-none whitespace-nowrap">TechMart</h1>
            <p className="text-white/40 text-[11px] font-mono mt-1 whitespace-nowrap">support console</p>
          </div>
          <div className="ml-auto flex items-center gap-1">
            <button
              onClick={onToggleCollapsed}
              className="w-7 h-7 rounded-md flex items-center justify-center hover:bg-white/10 transition-colors"
              aria-label="Collapse sidebar"
            >
              <PanelLeftClose size={15} className="text-white/50" />
            </button>
          </div>
        </div>

        <div className="px-4 pt-4">
          <button
            onClick={onNewChat}
            className="w-full flex items-center gap-2 px-3 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 border border-white/10 hover:border-white/20 text-sm font-medium text-white transition-all whitespace-nowrap"
          >
            <Plus size={16} className="shrink-0" />
            New conversation
          </button>
        </div>

        <div className="px-4 pt-3">
          <div className="relative">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-white/35" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search conversations"
              className="w-full pl-8 pr-3 py-2 rounded-lg bg-white/5 border border-white/10 text-xs text-white placeholder:text-white/30 outline-none focus:border-teal/50 focus:bg-white/10 transition-colors"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto px-3 mt-4 min-h-0">
          <p className="px-2 text-[10px] uppercase tracking-wider text-white/35 font-mono mb-2 whitespace-nowrap">
            Recent · auto-clears after 30 days
          </p>
          {filtered.length === 0 && (
            <p className="px-2 text-xs text-white/35">No conversations found</p>
          )}
          {filtered.map((s) => {
            const meta = AGENT_META[s.lastAgent] || null;
            const isConfirming = confirmDeleteId === s.id;
            return (
              <div
                key={s.id}
                onClick={() => onSelectSession(s.id)}
                onMouseLeave={() => isConfirming && setConfirmDeleteId(null)}
                className={`group w-full text-left px-3 py-2.5 rounded-xl mb-1 flex items-center gap-2.5 transition-all cursor-pointer ${
                  s.id === activeSessionId ? "bg-white/12 shadow-soft" : "hover:bg-white/[0.07]"
                }`}
              >
                <span
                  className="w-1 h-8 rounded-full shrink-0 transition-colors"
                  style={{ backgroundColor: meta ? meta.color : "rgba(255,255,255,0.15)" }}
                />
                <span className="min-w-0 flex-1">
                  <span
                    className={`block text-[13px] truncate ${
                      s.id === activeSessionId ? "text-white" : "text-white/65 group-hover:text-white/90"
                    }`}
                  >
                    {s.preview || "New conversation"}
                  </span>
                  {meta && (
                    <span className="block text-[10px] text-white/35 font-mono mt-0.5">
                      {s.lastAgent}
                    </span>
                  )}
                </span>
                <button
                  onClick={(e) => handleDeleteClick(e, s.id)}
                  className={`shrink-0 w-6 h-6 rounded-md flex items-center justify-center transition-all ${
                    isConfirming
                      ? "bg-amber/90 text-navy opacity-100"
                      : "opacity-0 group-hover:opacity-100 hover:bg-white/15 text-white/50"
                  }`}
                  aria-label={isConfirming ? "Confirm delete" : "Delete conversation"}
                  title={isConfirming ? "Click again to confirm" : "Delete conversation"}
                >
                  <Trash2 size={12} />
                </button>
              </div>
            );
          })}
        </div>

        <div className="px-5 py-4 border-t border-white/10">
          <p className="text-[10px] uppercase tracking-wider text-white/35 font-mono mb-2.5 whitespace-nowrap">
            Agent roster
          </p>
          <div className="grid grid-cols-2 gap-y-1.5 mb-4">
            {Object.entries(AGENT_META).map(([name, meta]) => {
              const Icon = meta.icon;
              return (
                <div key={name} className="flex items-center gap-1.5">
                  <Icon size={12} style={{ color: meta.color }} />
                  <span className="text-[11px] text-white/55">{name}</span>
                </div>
              );
            })}
          </div>

          <button
            onClick={handleThemeToggle}
            className="w-full flex items-center justify-between px-3 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 transition-colors"
          >
            <span className="flex items-center gap-2 text-[12px] text-white/70 whitespace-nowrap">
              <ThemeIcon size={13} className={themeIconFlip ? "icon-flip" : ""} />
              {theme === "light" ? "Light mode" : "Dark mode"}
            </span>
            <span
              className={`w-8 rounded-full relative transition-colors shrink-0 ${theme === "dark" ? "bg-teal" : "bg-white/20"}`}
              style={{ height: "18px" }}
            >
              <span
                className="absolute top-0.5 w-3.5 h-3.5 rounded-full bg-white transition-transform duration-300"
                style={{ left: "2px", transform: theme === "dark" ? "translateX(14px)" : "translateX(0)" }}
              />
            </span>
          </button>
        </div>
      </div>
    </aside>
  );
}
