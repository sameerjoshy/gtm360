export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    const url = new URL(request.url);

    if (url.pathname === "/health") {
      return json({ ok: true, service: "gtm360-llm-proxy", tier: "free" });
    }

    if (request.method === "POST" && url.pathname === "/research") {
      try {
        const { query } = await request.json();
        if (!query) return json({ error: "query required" }, 400);

        const webResult = await fetchWeb(query);
        return json({ query, webResult });
      } catch (e) {
        return json({ error: String(e) }, 500);
      }
    }

    if (request.method === "POST" && url.pathname === "/generate") {
      try {
        const { system, prompt } = await request.json();
        if (!prompt) return json({ error: "prompt required" }, 400);

        const out = await env.AI.run("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {
          messages: [
            { role: "system", content: system || "You are a helpful assistant." },
            { role: "user", content: prompt },
          ],
        });
        return json({ response: out?.response ?? out });
      } catch (e) {
        return json({ error: String(e) }, 500);
      }
    }

    return json({ error: "not found", paths: ["/health", "/research", "/generate"] }, 404);
  },
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
  });
}

async function fetchWeb(query) {
  // Free structured search: DuckDuckGo lite via textise dot iitty.
  const url = `https://r.jina.ai/http://html.duckduckgo.com/html/?q=${encodeURIComponent(query)}`;
  try {
    const resp = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0" } });
    if (!resp.ok) return { note: `search failed (${resp.status})` };
    const text = (await resp.text()).slice(0, 6000);
    return { text };
  } catch (e) {
    return { note: `search unavailable: ${e}` };
  }
}