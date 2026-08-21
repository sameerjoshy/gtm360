# GTM360 — Unified Revenue Operating System

One monorepo. One frontend. One backend. Six agents. No overlap.

## Why this exists

GTM-360 previously shipped many throwaway apps (gtm360-hq, gtm360-revenue-os,
gtm-360-workbench, gtm360-platform, gtmbrain, OpenSignal, crm-ai-analyst) — each
rebuilding the same control room in a different framework with scattered LLM,
Supabase, and HubSpot integrations. This repo is the consolidation:

| Concern | Standard | Runs on |
|---|---|---|
| Frontend | React 18 + Vite + Tailwind | Cloudflare Pages (free) |
| Backend | Python FastAPI + LangGraph | Render free (kept alive) |
| Data | Supabase (single project) | Supabase free |
| CRM | HubSpot (single adapter) | HubSpot free |
| LLM routing | DeepSeek / Groq / Gemini / Workers AI | free + pay-as-you-go |
| Edge | Cloudflare Workers | free tier |

## Repo layout

```
apps/web/        React + Vite + Tailwind cockpit (hq.gtm-360.com)
services/api/    FastAPI + LangGraph backend (all six agents)
workers/         Cloudflare Workers (llm-proxy, keepalive)
supabase/        SQL migrations + RPCs
```

## The six agents

1. **researcher** — company/domain → briefing (ARR, ICP fit, funding, signals, opener)
2. **hygiene** — CRM stale-deal & missing-field watchdog → fix suggestions
3. **sales** — deal intelligence: buyer readiness, stakeholders, risk, next actions
4. **content** — raw observation → drafted post/email with QC score + approval gate
5. **briefing** — weekly exec memo: pipeline pulse, OKRs, flags, one thing
6. **outbound** — buying-intent detection → personalized outreach drafts

## Run locally

Backend:

```bash
cd services/api
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env          # fill in keys
uvicorn app.main:app --reload
```

Frontend:

```bash
cd apps/web
npm install
npm run dev
```

Workers:

```bash
cd workers/llm-proxy
npx wrangler deploy
```

## Deploy

- Backend → Render (free web service, `services/api` as root)
- Frontend → Cloudflare Pages (build: `npm run build`, dir: `apps/web/dist`)
- Workers → `wrangler deploy` per worker
- Keepalive → scheduled Worker pings the Render service hourly