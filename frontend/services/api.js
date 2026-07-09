import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

export async function sendMessage(message, sessionId, userId = "guest") {
  const res = await api.post("/chat", {
    message,
    session_id: sessionId,
    user_id: userId,
  });
  return res.data;
}

export async function getSessionHistory(sessionId) {
  const res = await api.get(`/sessions/${sessionId}/history`);
  return res.data;
}

export async function register(email, password, name) {
  const res = await api.post("/auth/register", { email, password, name });
  return res.data;
}

export async function login(email, password) {
  const res = await api.post("/auth/login", { email, password });
  return res.data;
}

export default api;
