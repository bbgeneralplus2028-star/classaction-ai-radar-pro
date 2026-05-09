import requests

def fetch_latest_cases():

    url = "https://www.courtlistener.com/api/rest/v3/dockets/"

    params = {
        "page_size": 20,
        "ordering": "-date_created",
        "search": "class action"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30
        )

        data = response.json()

        results = data.get("results", [])

        cases = []

        for item in results:

            case_name = item.get("case_name") or item.get("caseName") or "Unknown Case"

            cases.append({
                "title": case_name,
                "court": str(item.get("court") or "Unknown Court"),
                "date": item.get("date_filed") or "",
                "url": item.get("absolute_url") or ""
            })

        return cases

    except Exception as e:
        print("COURTLISTENER ERROR:", str(e))
        return []
