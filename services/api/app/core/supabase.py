from app.core.config import settings


class SupabaseClient:
    """Single Supabase adapter used by every agent."""

    def __init__(self, use_service_role: bool = True):
        self._client = None
        self._use_service_role = use_service_role

    @property
    def client(self):
        if self._client is None:
            try:
                from supabase import create_client

                key = (
                    settings.supabase_service_role_key
                    if self._use_service_role
                    else settings.supabase_anon_key
                )
                self._client = create_client(settings.supabase_url, key)
            except Exception as exc:  # pragma: no cover
                raise RuntimeError(f"Supabase unavailable: {exc}") from exc
        return self._client

    def table(self, name: str):
        return self.client.table(name)

    def create_agent_run(
        self, agent_type: str, inputs: dict, workspace_id: str = None
    ) -> str:
        """Insert an agent_run row, returning the run_id."""
        run = (
            self.table("agent_runs")
            .insert(
                {
                    "workspace_id": workspace_id or settings.workspace_id,
                    "agent_type": agent_type,
                    "status": "RUNNING",
                    "inputs": inputs,
                }
            )
            .execute()
        )
        return run.data[0]["run_id"]

    def finish_agent_run(self, run_id: str, outputs: dict, status: str = "COMPLETED"):
        self.table("agent_runs").update({"status": status, "outputs": outputs}).eq(
            "run_id", run_id
        ).execute()

    def upsert(self, table: str, rows: list):
        return self.table(table).upsert(rows).execute()


supabase_client = SupabaseClient()