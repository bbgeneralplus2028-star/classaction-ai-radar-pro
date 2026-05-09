import requests

BASE_URL = "https://www.courtlistener.com/api/rest/v4/search/"

def fetch_latest_cases():
    try:
        params = {
            "q": "class action lawsuit",
            "type": "o",  # opinions
            "order_by": "score desc"
        }

        response = requests.get(BASE_URL, params=params, timeout=15)

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print("API ERROR")
            return []

        data = response.json()

        results = data.get("results", [])

        cases = []

        for item in results:
            cases.append({
                "title": item.get("caseName") or item.get("case_name") or "Unknown",
                "court": item.get("court") or "Unknown",
                "date": item.get("dateFiled") or "",
                "url": item.get("absolute_url") or ""
            })

        print("FOUND CASES:", len(cases))

        return cases

    except Exception as e:
        print("FETCH ERROR:", e)
        return []
