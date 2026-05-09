import requests

def fetch_latest_cases():
    try:
        url = "https://www.courtlistener.com/api/rest/v4/opinions/"

        params = {
            "order_by": "-date_created",
            "page_size": 20
        }

        r = requests.get(url, params=params, timeout=15)

        print("API STATUS:", r.status_code)

        if r.status_code != 200:
            return []

        data = r.json().get("results", [])

        cases = []

        for item in data:
            cases.append({
                "title": item.get("caseName") or "Unknown Case",
                "court": str(item.get("court") or "Unknown"),
                "filed_date": item.get("date_created") or "",
                "url": item.get("absolute_url") or "",
                "summary": item.get("snippet") or "",
                "source": "courtlistener",
                "category": "legal"
            })

        print("FOUND CASES:", len(cases))

        return cases

    except Exception as e:
        print("FETCH ERROR:", e)
        return []
