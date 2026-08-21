"""Demo workspace data.

When an agent runs with workspace_id == "demo", it reads from this seeded,
anonymised dataset instead of the live HubSpot account. This makes the
Operator's Desk genuinely usable by visitors without touching real data.
"""

DEMO_DEALS = [
    {
        "id": "demo-1001",
        "properties": {
            "dealname": "Northwind Analytics — FCRO",
            "amount": "20000",
            "dealstage": "appointmentscheduled",
            "closedate": None,
            "days_in_stage": "3",
            "hubspot_owner_id": "owner-1",
            "hs_lastmodifieddate": None,
            "associatedcompanyid": "demo-c1",
        },
    },
    {
        "id": "demo-1002",
        "properties": {
            "dealname": "Lumen Grid — DIAG",
            "amount": "8000",
            "dealstage": "presentationscheduled",
            "closedate": None,
            "days_in_stage": "9",
            "hubspot_owner_id": "",
            "hs_lastmodifieddate": None,
            "associatedcompanyid": "demo-c2",
        },
    },
    {
        "id": "demo-1003",
        "properties": {
            "dealname": "Beaconline — ROPS",
            "amount": "5000",
            "dealstage": "contractsent",
            "closedate": None,
            "days_in_stage": "21",
            "hubspot_owner_id": "owner-1",
            "hs_lastmodifieddate": None,
            "associatedcompanyid": "demo-c3",
        },
    },
    {
        "id": "demo-1004",
        "properties": {
            "dealname": "Meridian Health — FCRO",
            "amount": "15000",
            "dealstage": "appointmentscheduled",
            "closedate": None,
            "days_in_stage": "2",
            "hubspot_owner_id": "owner-2",
            "hs_lastmodifieddate": None,
            "associatedcompanyid": "demo-c4",
        },
    },
    {
        "id": "demo-1005",
        "properties": {
            "dealname": "Summitworks — DIAG",
            "amount": "4000",
            "dealstage": "decisionmakerboughtin",
            "closedate": None,
            "days_in_stage": "34",
            "hubspot_owner_id": "",
            "hs_lastmodifieddate": None,
            "associatedcompanyid": "demo-c5",
        },
    },
    {
        "id": "demo-1006",
        "properties": {
            "dealname": "Fieldpine — DIAG",
            "amount": "3000",
            "dealstage": "appointmentscheduled",
            "closedate": None,
            "days_in_stage": "1",
            "hubspot_owner_id": "owner-1",
            "hs_lastmodifieddate": None,
            "associatedcompanyid": "demo-c6",
        },
    },
    {
        "id": "demo-1007",
        "properties": {
            "dealname": "Cobalt Bay — ROPS",
            "amount": "12000",
            "dealstage": "appointmentscheduled",
            "closedate": None,
            "days_in_stage": "18",
            "hubspot_owner_id": "owner-2",
            "hs_lastmodifieddate": None,
            "associatedcompanyid": "demo-c7",
        },
    },
    {
        "id": "demo-1008",
        "properties": {
            "dealname": "Harborstep — DIAG",
            "amount": "6000",
            "dealstage": "appointmentscheduled",
            "closedate": None,
            "days_in_stage": "12",
            "hubspot_owner_id": "owner-1",
            "hs_lastmodifieddate": None,
            "associatedcompanyid": "demo-c8",
        },
    },
]

DEMO_COMPANIES = {
    "demo-c1": {"id": "demo-c1", "properties": {"name": "Northwind Analytics", "domain": "northwindanalytics.io", "hs_annual_revenue": "15000000", "numberofemployees": "48"}},
    "demo-c2": {"id": "demo-c2", "properties": {"name": "Lumen Grid", "domain": "lumengrid.com", "hs_annual_revenue": "9000000", "numberofemployees": "31"}},
    "demo-c3": {"id": "demo-c3", "properties": {"name": "Beaconline", "domain": "beaconline.io", "hs_annual_revenue": "24000000", "numberofemployees": "120"}},
    "demo-c4": {"id": "demo-c4", "properties": {"name": "Meridian Health", "domain": "meridianhealth.ai", "hs_annual_revenue": "32000000", "numberofemployees": "210"}},
    "demo-c5": {"id": "demo-c5", "properties": {"name": "Summitworks", "domain": "summitworks.co", "hs_annual_revenue": "6000000", "numberofemployees": "22"}},
    "demo-c6": {"id": "demo-c6", "properties": {"name": "Fieldpine", "domain": "fieldpine.com", "hs_annual_revenue": "11000000", "numberofemployees": "40"}},
    "demo-c7": {"id": "demo-c7", "properties": {"name": "Cobalt Bay", "domain": "cobaltbay.io", "hs_annual_revenue": "27000000", "numberofemployees": "160"}},
    "demo-c8": {"id": "demo-c8", "properties": {"name": "Harborstep", "domain": "harborstep.com", "hs_annual_revenue": "8000000", "numberofemployees": "27"}},
}

DEMO_OKRS = [
    {
        "quarter": "Q3 2026",
        "objective_number": 1,
        "objective_text": "Get the first three paying clients",
        "krs": [
            {"kr_number": 1, "kr_text": "10 discovery calls", "target": 10, "current": 3},
            {"kr_number": 2, "kr_text": "3 proposals sent", "target": 3, "current": 1},
            {"kr_number": 3, "kr_text": "1 signed engagement", "target": 1, "current": 0},
        ],
    },
    {
        "quarter": "Q3 2026",
        "objective_number": 2,
        "objective_text": "Build awareness and thought leadership",
        "krs": [
            {"kr_number": 1, "kr_text": "20 LinkedIn posts", "target": 20, "current": 7},
            {"kr_number": 2, "kr_text": "500 LinkedIn followers", "target": 500, "current": 180},
            {"kr_number": 3, "kr_text": "100 newsletter subscribers", "target": 100, "current": 32},
        ],
    },
    {
        "quarter": "Q3 2026",
        "objective_number": 3,
        "objective_text": "Build the GTM-360 system",
        "krs": [
            {"kr_number": 1, "kr_text": "Six agents operational", "target": 6, "current": 6},
            {"kr_number": 2, "kr_text": "Weekly briefings running", "target": 1, "current": 1},
            {"kr_number": 3, "kr_text": "Zero manual entry", "target": 1, "current": 0},
        ],
    },
]

DEMO_ESCALATIONS = [
    {
        "raised_by": "Researcher",
        "escalation_type": "pipeline_quality",
        "description": "Two live deals have no recorded close date and no owner assigned.",
        "decision_needed": "Assign owners and set expected close dates.",
        "sams_recommendation": "Prioritise Cobalt Bay — highest value without an owner.",
        "status": "OPEN",
    },
    {
        "raised_by": "Hygiene",
        "escalation_type": "data_quality",
        "description": "CRM health score at 0.61 — 30% of deals missing owner or close date.",
        "decision_needed": "Run a hygiene pass or accept the current state.",
        "sams_recommendation": "Run hygiene before the next forecast call.",
        "status": "OPEN",
    },
]

DEMO_PIPELINE = [
    {
        "deal_id": "demo-1001", "deal_name": "Northwind Analytics — FCRO",
        "company_name": "Northwind Analytics", "company_domain": "northwindanalytics.io",
        "contact_name": "Priya Nair", "contact_email": "priya@northwindanalytics.io",
        "stage": "appointmentscheduled", "amount": 20000, "days_in_stage": 3,
        "icp_score": 7.4, "icp_fit": "STRONG", "service_line": "FCRO",
    },
    {
        "deal_id": "demo-1002", "deal_name": "Lumen Grid — DIAG",
        "company_name": "Lumen Grid", "company_domain": "lumengrid.com",
        "contact_name": "Tom Becker", "contact_email": "tom@lumengrid.com",
        "stage": "presentationscheduled", "amount": 8000, "days_in_stage": 9,
        "icp_score": 6.2, "icp_fit": "MODERATE", "service_line": "DIAG",
    },
    {
        "deal_id": "demo-1003", "deal_name": "Beaconline — ROPS",
        "company_name": "Beaconline", "company_domain": "beaconline.io",
        "contact_name": "Anna Kim", "contact_email": "anna@beaconline.io",
        "stage": "contractsent", "amount": 5000, "days_in_stage": 21,
        "icp_score": 5.8, "icp_fit": "MODERATE", "service_line": "ROPS",
    },
    {
        "deal_id": "demo-1004", "deal_name": "Meridian Health — FCRO",
        "company_name": "Meridian Health", "company_domain": "meridianhealth.ai",
        "contact_name": "Raj Patel", "contact_email": "raj@meridianhealth.ai",
        "stage": "appointmentscheduled", "amount": 15000, "days_in_stage": 2,
        "icp_score": 8.1, "icp_fit": "STRONG", "service_line": "FCRO",
    },
    {
        "deal_id": "demo-1005", "deal_name": "Summitworks — DIAG",
        "company_name": "Summitworks", "company_domain": "summitworks.co",
        "contact_name": "Leo Moreau", "contact_email": "leo@summitworks.co",
        "stage": "decisionmakerboughtin", "amount": 4000, "days_in_stage": 34,
        "icp_score": 4.9, "icp_fit": "WEAK", "service_line": "DIAG",
    },
    {
        "deal_id": "demo-1006", "deal_name": "Fieldpine — DIAG",
        "company_name": "Fieldpine", "company_domain": "fieldpine.com",
        "contact_name": "Sara Owen", "contact_email": "sara@fieldpine.com",
        "stage": "appointmentscheduled", "amount": 3000, "days_in_stage": 1,
        "icp_score": 6.9, "icp_fit": "MODERATE", "service_line": "DIAG",
    },
    {
        "deal_id": "demo-1007", "deal_name": "Cobalt Bay — ROPS",
        "company_name": "Cobalt Bay", "company_domain": "cobaltbay.io",
        "contact_name": "David Lin", "contact_email": "david@cobaltbay.io",
        "stage": "appointmentscheduled", "amount": 12000, "days_in_stage": 18,
        "icp_score": 7.0, "icp_fit": "MODERATE", "service_line": "ROPS",
    },
    {
        "deal_id": "demo-1008", "deal_name": "Harborstep — DIAG",
        "company_name": "Harborstep", "company_domain": "harborstep.com",
        "contact_name": "Mina Choi", "contact_email": "mina@harborstep.com",
        "stage": "appointmentscheduled", "amount": 6000, "days_in_stage": 12,
        "icp_score": 6.6, "icp_fit": "MODERATE", "service_line": "DIAG",
    },
]


def is_demo(state: dict) -> bool:
    return state.get("workspace_id", "default") == "demo"


def demo_deals() -> list:
    return DEMO_DEALS


def demo_company(company_id: str) -> dict:
    return DEMO_COMPANIES.get(company_id, {})