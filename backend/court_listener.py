import requests

URL = "https://www.courtlistener.com/api/rest/v4/opinions/"

def fetch_latest_cases():
    try:
        params = {
            "order_by": "-date_created",
            "page_size": 20,
            "q": "settlement OR lawsuit OR class action"
        }

        r = requests.get(URL, params=params, timeout=15)

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            return []

        data = r.json()
        results = data.get("results", [])

        cases = []

        for item in results:
            cases.append({
                "title": item.get("caseName") or "Unknown Case",
                "court": str(item.get("court") or "Unknown"),
                "date": item.get("date_created") or "",
                "url": item.get("absolute_url") or ""
            })

        print("FOUND:", len(cases))

        return cases

    except Exception as e:
        print("ERROR:", e)
        return []
