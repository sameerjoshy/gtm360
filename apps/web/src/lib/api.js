const API_URL = import.meta.env.VITE_API_URL || "";

export async function runAgent(agent, body) {
  const res = await fetch(`${API_URL}/api/v1/agents/${agent}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed (${res.status})`);
  }
  return res.json();
}