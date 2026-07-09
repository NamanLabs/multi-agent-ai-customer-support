import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

const THIRTY_DAYS_MS = 30 * 24 * 60 * 60 * 1000;

function generateSessionId() {
  return (
    "sess-" +
    Date.now().toString(36) +
    "-" +
    Math.random().toString(36).slice(2, 10)
  );
}

export default function Home() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [messagesBySession, setMessagesBySession] = useState({});
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [theme, setTheme] = useState("light");
  const [hydrated, setHydrated] = useState(false);

  // Load persisted state on first mount, purging any session older than 30 days
  useEffect(() => {
    const savedSessions = window.localStorage.getItem("techmart_sessions");
    const savedMessages = window.localStorage.getItem("techmart_messages");
    const savedCollapsed = window.localStorage.getItem("techmart_sidebar_collapsed");
    const savedTheme = window.localStorage.getItem("techmart_theme");

    let parsedSessions = savedSessions ? JSON.parse(savedSessions) : [];
    let parsedMessages = savedMessages ? JSON.parse(savedMessages) : {};

    const now = Date.now();
    const freshSessions = parsedSessions.filter(
      (s) => !s.createdAt || now - s.createdAt < THIRTY_DAYS_MS
    );
    if (freshSessions.length !== parsedSessions.length) {
      const keptIds = new Set(freshSessions.map((s) => s.id));
      parsedMessages = Object.fromEntries(
        Object.entries(parsedMessages).filter(([id]) => keptIds.has(id))
      );
    }

    setSessions(freshSessions);
    setMessagesBySession(parsedMessages);
    if (savedCollapsed) setSidebarCollapsed(JSON.parse(savedCollapsed));
    if (savedTheme) setTheme(savedTheme);

    if (freshSessions.length > 0) {
      setActiveSessionId(freshSessions[0].id);
    } else {
      const id = generateSessionId();
      setSessions([{ id, preview: "New conversation", createdAt: now }]);
      setMessagesBySession((prev) => ({ ...prev, [id]: [] }));
      setActiveSessionId(id);
    }
    setHydrated(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Apply theme class to <html> and persist
  useEffect(() => {
    if (!hydrated) return;
    document.documentElement.classList.toggle("dark", theme === "dark");
    window.localStorage.setItem("techmart_theme", theme);
  }, [theme, hydrated]);

  useEffect(() => {
    if (!hydrated) return;
    window.localStorage.setItem("techmart_sidebar_collapsed", JSON.stringify(sidebarCollapsed));
  }, [sidebarCollapsed, hydrated]);

  // Persist sessions/messages whenever they change
  useEffect(() => {
    if (!hydrated) return;
    window.localStorage.setItem("techmart_sessions", JSON.stringify(sessions));
    window.localStorage.setItem("techmart_messages", JSON.stringify(messagesBySession));
  }, [sessions, messagesBySession, hydrated]);

  function handleNewChat() {
    const id = generateSessionId();
    setSessions((prev) => [{ id, preview: "New conversation", createdAt: Date.now() }, ...prev]);
    setMessagesBySession((prev) => ({ ...prev, [id]: [] }));
    setActiveSessionId(id);
  }

  function handleDeleteSession(id) {
    setSessions((prev) => {
      const next = prev.filter((s) => s.id !== id);
      if (id === activeSessionId) {
        if (next.length > 0) {
          setActiveSessionId(next[0].id);
        } else {
          const newId = generateSessionId();
          setMessagesBySession((prevMsgs) => ({ ...prevMsgs, [newId]: [] }));
          setActiveSessionId(newId);
          return [{ id: newId, preview: "New conversation", createdAt: Date.now() }];
        }
      }
      return next;
    });
    setMessagesBySession((prev) => {
      const next = { ...prev };
      delete next[id];
      return next;
    });
  }

  function setMessagesForActiveSession(updater) {
    setMessagesBySession((prev) => {
      const current = prev[activeSessionId] || [];
      const next = typeof updater === "function" ? updater(current) : updater;

      const firstUserMsg = next.find((m) => m.role === "user");
      const lastAssistantMsg = [...next].reverse().find((m) => m.role === "assistant");
      const lastAgent = lastAssistantMsg?.agentsInvoked?.[0]
        ?.replace(" Agent", "")
        ?.replace(" Support", "");

      if (firstUserMsg) {
        setSessions((prevSessions) =>
          prevSessions.map((s) =>
            s.id === activeSessionId
              ? { ...s, preview: firstUserMsg.text.slice(0, 40), lastAgent: lastAgent || s.lastAgent }
              : s
          )
        );
      }

      return { ...prev, [activeSessionId]: next };
    });
  }

  if (!activeSessionId) return null;

  return (
    <div className="flex h-screen w-screen overflow-hidden">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={setActiveSessionId}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
        collapsed={sidebarCollapsed}
        onToggleCollapsed={() => setSidebarCollapsed((v) => !v)}
        theme={theme}
        onToggleTheme={() => setTheme((t) => (t === "light" ? "dark" : "light"))}
      />
      <main className="flex-1 min-w-0">
        <ChatWindow
          sessionId={activeSessionId}
          messages={messagesBySession[activeSessionId] || []}
          setMessages={setMessagesForActiveSession}
        />
      </main>
    </div>
  );
}
