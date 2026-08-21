-- GTM360 unified schema
-- Core tables consumed by the six agents.

create extension if not exists "pgcrypto";

-- Agent run ledger (written by every agent via app/core/supabase.py)
create table if not exists public.agent_runs (
    run_id uuid primary key default gen_random_uuid(),
    workspace_id text not null default 'default',
    agent_type text not null,
    status text not null default 'RUNNING',
    inputs jsonb default '{}'::jsonb,
    outputs jsonb default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists agent_runs_agent_type_idx on public.agent_runs (agent_type);
create index if not exists agent_runs_workspace_idx on public.agent_runs (workspace_id);

-- Pipeline snapshot (mirrors HubSpot; fed by hygiene agent + sync automation)
create table if not exists public.pipeline_snapshot (
    deal_id text primary key,
    deal_name text,
    company_name text,
    company_domain text,
    contact_name text,
    contact_email text,
    stage text,
    amount numeric default 0,
    close_date date,
    days_in_stage int default 0,
    last_activity_date date,
    icp_score numeric default 0,
    icp_fit text,
    service_line text,
    signal text,
    snapshot_date date not null default current_date
);

-- OKR tracker
create table if not exists public.okr_tracker (
    id uuid primary key default gen_random_uuid(),
    quarter text,
    objective_number int,
    objective_text text,
    kr_number int,
    kr_text text,
    kr_target numeric default 0,
    kr_current numeric default 0,
    status text default 'OPEN'
);

-- Escalations
create table if not exists public.escalations (
    id uuid primary key default gen_random_uuid(),
    raised_by text,
    escalation_type text,
    description text,
    decision_needed text,
    sams_recommendation text,
    sameer_decision text,
    status text default 'OPEN',
    created_at timestamptz not null default now()
);

-- Hygiene scans output
create table if not exists public.hygiene_scans (
    id uuid primary key default gen_random_uuid(),
    workspace_id text not null default 'default',
    health_score numeric default 0,
    issue_count int default 0,
    issues jsonb default '[]'::jsonb,
    scanned_at timestamptz not null default now()
);

-- Content queue (written by content agent, gated on approval)
create table if not exists public.content_queue (
    id uuid primary key default gen_random_uuid(),
    workspace_id text not null default 'default',
    raw_observation text,
    post_format text,
    channel text default 'linkedin',
    draft text,
    qc_score numeric default 0,
    qc_notes text,
    status text default 'AWAITING_APPROVAL',
    approved_at timestamptz,
    published_at timestamptz,
    created_at timestamptz not null default now()
);

-- Outbound sequences
create table if not exists public.outbound_sequences (
    id uuid primary key default gen_random_uuid(),
    workspace_id text not null default 'default',
    domain text,
    intent_score numeric default 0,
    intent text,
    matched_signals jsonb default '[]'::jsonb,
    sequence jsonb default '[]'::jsonb,
    status text default 'DRAFT',
    created_at timestamptz not null default now()
);

-- Enable RLS, default closed; the backend uses service role so it bypasses.
alter table public.agent_runs enable row level security;
alter table public.pipeline_snapshot enable row level security;
alter table public.okr_tracker enable row level security;
alter table public.escalations enable row level security;
alter table public.hygiene_scans enable row level security;
alter table public.content_queue enable row level security;
alter table public.outbound_sequences enable row level security;