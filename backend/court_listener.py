import requests

COURTLISTENER_URL = "https://www.courtlistener.com/api/rest/v4/opinions/"

def fetch_latest_cases():
    try:
        print("🔎 Fetching real cases from CourtListener...")

        params = {
            "order_by": "-date_created",
            "page_size": 20
        }

        response = requests.get(COURTLISTENER_URL, params=params, timeout=15)

        print("STATUS CODE:", response.status_code)

        if response.status_code != 200:
            print("FAILED API RESPONSE")
            return []

        data = response.json()

        results = data.get("results", [])

        cases = []

        for item in results:
            cases.append({
                "title": item.get("caseName") or "Unknown Case",
                "court": item.get("court") or "Unknown Court",
                "date": item.get("date_created") or "",
                "url": item.get("absolute_url") or ""
            })

        print(f"FOUND {len(cases)} CASES")

        return cases

    except Exception as e:
        print("FETCH ERROR:", e)
        return []
