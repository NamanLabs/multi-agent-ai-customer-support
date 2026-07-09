import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";
import { sendMessage } from "../services/api";

const SUGGESTIONS = [
  "Where's my order?",
  "I want a refund",
  "My login isn't working",
  "What's the warranty on laptops?",
];

export default function ChatWindow({ sessionId, messages, setMessages }) {
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState(null);
  const scrollRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isTyping]);

  async function submitMessage(text) {
    if (!text || isTyping) return;

    setError(null);
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text, timestamp: Date.now() }]);
    setIsTyping(true);

    try {
      const data = await sendMessage(text, sessionId);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.response,
          agentsInvoked: data.agents_invoked,
          confidence: data.confidence,
          escalated: data.escalated,
          timestamp: Date.now(),
        },
      ]);
    } catch (err) {
      setError(
        "Couldn't reach the support backend. Check that the FastAPI server is running on localhost:8000."
      );
    } finally {
      setIsTyping(false);
    }
  }

  function handleSend(e) {
    e.preventDefault();
    submitMessage(input.trim());
  }

  return (
    <div className="flex flex-col h-full bg-paper dark:bg-paper-dark relative overflow-hidden transition-colors">
      <header className="px-6 py-4 border-b border-gray-200 dark:border-white/10 bg-white/90 dark:bg-card-dark/90 backdrop-blur-sm z-10 flex items-center justify-between transition-colors">
        <div>
          <h2 className="font-display font-semibold text-ink dark:text-ink-dark text-base">Customer support</h2>
          <p className="text-[11px] text-muted dark:text-muted-dark font-mono mt-0.5">
            session · {sessionId.slice(0, 12)}
          </p>
        </div>
      </header>

      <div className="circuit-bg" />

      <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-6 relative z-[1]">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center px-8">
            <div className="w-12 h-12 rounded-2xl bg-navy/5 dark:bg-white/5 border border-navy/10 dark:border-white/10 flex items-center justify-center mb-4">
              <div className="w-4 h-4 rounded-sm bg-navy/70 dark:bg-teal/70" />
            </div>
            <p className="font-display text-lg text-ink/85 dark:text-ink-dark/90 mb-1.5">How can we help?</p>
            <p className="text-sm text-muted dark:text-muted-dark max-w-sm mb-6">
              Ask about billing, orders, product info, or anything else — the right
              specialist agent picks it up automatically.
            </p>
            <div className="flex flex-wrap gap-2 justify-center max-w-md">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => submitMessage(s)}
                  className="px-3 py-1.5 rounded-full border border-gray-300 dark:border-white/15 bg-white dark:bg-card-dark text-xs text-ink/70 dark:text-ink-dark/70 hover:border-navy/40 dark:hover:border-teal/50 hover:text-navy dark:hover:text-teal transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m, i) => (
          <MessageBubble key={i} message={m} />
        ))}
        {isTyping && <TypingIndicator />}
      </div>

      {error && (
        <div className="mx-6 mb-2 px-3 py-2 bg-amber/10 border border-amber/30 text-amber-700 dark:text-amber-400 text-xs rounded-lg relative z-[1]">
          {error}
        </div>
      )}

      <form onSubmit={handleSend} className="px-6 py-4 border-t border-gray-200 dark:border-white/10 bg-white dark:bg-card-dark flex gap-3 relative z-[1] transition-colors">
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your issue..."
          className="flex-1 px-4 py-2.5 rounded-full border border-gray-300 dark:border-white/15 bg-white dark:bg-paper-dark text-ink dark:text-ink-dark text-sm font-body outline-none focus:border-teal focus:shadow-glow transition-shadow placeholder:text-muted dark:placeholder:text-muted-dark"
        />
        <button
          type="submit"
          disabled={!input.trim() || isTyping}
          className="w-10 h-10 rounded-full bg-navy text-white flex items-center justify-center disabled:opacity-30 hover:bg-navy-light active:scale-95 transition-all shrink-0"
          aria-label="Send message"
        >
          <Send size={16} />
        </button>
      </form>
    </div>
  );
}
