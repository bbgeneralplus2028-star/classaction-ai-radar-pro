import requests
from datetime import datetime

COURTLISTENER_API = "https://www.courtlistener.com/api/rest/v3/dockets/"

def fetch_latest_cases(limit=20):
    """
    Pull latest federal docket cases (including class actions when tagged).
    """

    try:
        response = requests.get(
            COURTLISTENER_API,
            params={"page_size": limit},
            timeout=10
        )

        data = response.json()

        results = []

        for item in data.get("results", []):
            results.append({
                "title": item.get("case_name"),
                "court": item.get("court"),
                "filed_date": item.get("date_filed"),
                "url": item.get("absolute_url"),
                "summary": item.get("case_name_full"),
                "source": "CourtListener",
                "fetched_at": str(datetime.utcnow())
            })

        return results

    except Exception as e:
        return [{"error": str(e)}]
