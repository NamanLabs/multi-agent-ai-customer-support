import { CreditCard, Wrench, Package, AlertTriangle, HelpCircle, Sparkles } from "lucide-react";
import RoutingReceipt from "./RoutingReceipt";

const AGENT_ICON = {
  "Billing Agent": { icon: CreditCard, color: "#1E3A5F" },
  "Technical Support Agent": { icon: Wrench, color: "#008C80" },
  "Product Agent": { icon: Package, color: "#6D4FA8" },
  "Complaint Agent": { icon: AlertTriangle, color: "#B5760C" },
  "FAQ Agent": { icon: HelpCircle, color: "#5B6270" },
};

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export default function MessageBubble({ message }) {
  const isUser = message.role === "user";
  const time = formatTime(message.timestamp ? new Date(message.timestamp) : new Date());

  if (isUser) {
    return (
      <div className="flex justify-end mb-5 animate-fade-up">
        <div className="max-w-md">
          <div className="bg-navy text-white rounded-2xl rounded-br-md px-4 py-2.5 font-body text-[13.5px] shadow-soft">
            {message.text}
          </div>
          <p className="text-[10px] text-muted dark:text-muted-dark text-right mt-1 pr-1">{time}</p>
        </div>
      </div>
    );
  }

  const primaryAgent = message.agentsInvoked?.[0];
  const meta = AGENT_ICON[primaryAgent];
  const Icon = meta?.icon || Sparkles;
  const iconColor = meta?.color || "#1E3A5F";

  return (
    <div className="flex justify-start mb-5 gap-2.5 animate-fade-up">
      <div
        className="w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5 border"
        style={{ backgroundColor: `${iconColor}14`, borderColor: `${iconColor}30` }}
      >
        <Icon size={13} style={{ color: iconColor }} />
      </div>
      <div className="max-w-md min-w-0">
        <div
          className="bg-white dark:bg-card-dark rounded-2xl rounded-bl-md px-4 py-2.5 font-body text-[13.5px] text-ink dark:text-ink-dark shadow-soft border-l-2 transition-colors"
          style={{ borderLeftColor: iconColor }}
        >
          {message.text}
        </div>
        <p className="text-[10px] text-muted dark:text-muted-dark mt-1 pl-1">{time}</p>
        {message.agentsInvoked && (
          <RoutingReceipt
            agentsInvoked={message.agentsInvoked}
            confidence={message.confidence}
            escalated={message.escalated}
          />
        )}
      </div>
    </div>
  );
}
