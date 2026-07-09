import { Sparkles } from "lucide-react";

export default function TypingIndicator() {
  return (
    <div className="flex justify-start mb-5 gap-2.5 animate-fade-up">
      <div className="w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5 border bg-navy/5 dark:bg-white/5 border-navy/15 dark:border-white/15">
        <Sparkles size={13} className="text-navy/60 dark:text-teal/70" />
      </div>
      <div className="bg-white dark:bg-card-dark border border-gray-100 dark:border-white/10 rounded-2xl rounded-bl-md px-4 py-3 flex items-center gap-1.5 shadow-soft transition-colors">
        <span className="w-1.5 h-1.5 rounded-full bg-navy/40 dark:bg-teal/50 typing-dot" style={{ animationDelay: "0s" }} />
        <span className="w-1.5 h-1.5 rounded-full bg-navy/40 dark:bg-teal/50 typing-dot" style={{ animationDelay: "0.15s" }} />
        <span className="w-1.5 h-1.5 rounded-full bg-navy/40 dark:bg-teal/50 typing-dot" style={{ animationDelay: "0.3s" }} />
      </div>
    </div>
  );
}
