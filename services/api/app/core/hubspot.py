import httpx

from app.core.config import settings


class HubSpotAdapter:
    """Single HubSpot adapter shared by all agents."""

    BASE_URL = "https://api.hubapi.com"

    def __init__(self):
        self._token = settings.hubspot_access_token
        self._api_key = settings.hubspot_api_key

    @property
    def _headers(self) -> dict:
        if self._token:
            return {"Authorization": f"Bearer {self._token}"}
        return {"Authorization": f"Bearer {self._api_key}"}

    async def _get(self, path: str, params: dict | None = None) -> dict:
        async with httpx.AsyncClient(base_url=self.BASE_URL, timeout=30) as client:
            resp = await client.get(path, params=params, headers=self._headers)
            resp.raise_for_status()
            return resp.json()

    async def _post(self, path: str, body: dict) -> dict:
        async with httpx.AsyncClient(base_url=self.BASE_URL, timeout=30) as client:
            resp = await client.post(path, json=body, headers=self._headers)
            resp.raise_for_status()
            return resp.json()

    async def search_companies(self, domain: str) -> list:
        body = {
            "filterGroups": [
                {"filters": [{"propertyName": "domain", "operator": "EQ", "value": domain}]}
            ],
            "properties": ["name", "domain", "hs_annual_revenue", "numberofemployees", "website"],
        }
        data = await self._post("/crm/v3/objects/companies/search", body)
        return data.get("results", [])

    async def search_deals(self, limit: int = 50) -> list:
        body = {
            "limit": limit,
            "properties": [
                "dealname",
                "amount",
                "dealstage",
                "closedate",
                "hs_lastmodifieddate",
                "hs_createdate",
                "hubspot_owner_id",
                "days_in_stage",
            ],
        }
        data = await self._post("/crm/v3/objects/deals/search", body)
        return data.get("results", [])

    async def read_company(self, company_id: str) -> dict:
        return await self._get(f"/crm/v3/objects/companies/{company_id}")

    async def write_properties(self, object_type: str, record_id: str, props: dict):
        return await self._post(
            f"/crm/v3/objects/{object_type}/{record_id}", {"properties": props}
        )


hubspot = HubSpotAdapter()