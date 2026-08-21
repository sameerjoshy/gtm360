import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    environment: str = os.getenv("ENVIRONMENT", "development")
    workspace_id: str = os.getenv("WORKSPACE_ID", "default")

    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_anon_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # HubSpot
    hubspot_api_key: str = os.getenv("HUBSPOT_API_KEY", "")
    hubspot_access_token: str = os.getenv("HUBSPOT_ACCESS_TOKEN", "")

    # LLM providers (free-first)
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    deepseek_model_id: str = os.getenv("DEEPSEEK_MODEL_ID", "deepseek-chat")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Edge
    llm_proxy_url: str = os.getenv(
        "LLM_PROXY_URL", "https://gtm360-llm-proxy.sameerjoshy.workers.dev"
    )

    # Email
    sender_email: str = os.getenv("SENDER_EMAIL", "sameer@gtm-360.com")

    @property
    def llm_ready(self) -> bool:
        return any(
            [
                self.deepseek_api_key,
                self.groq_api_key,
                self.gemini_api_key,
                self.anthropic_api_key,
            ]
        )


settings = Settings()