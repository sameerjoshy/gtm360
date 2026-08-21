export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(ping(env));
  },

  async fetch(request, env) {
    await ping(env);
    return new Response("pong", { status: 200 });
  },
};

async function ping(env) {
  const url = env.RENDER_API_URL || "https://gtm360-api.onrender.com";
  try {
    const resp = await fetch(`${url}/api/v1/health`, { signal: AbortSignal.timeout(15000) });
    return resp.ok;
  } catch (e) {
    console.log("keepalive ping failed", e);
    return false;
  }
}