import requests

def fetch_latest_cases():

    url = "https://www.courtlistener.com/api/rest/v3/dockets/"

    params = {
        "page_size": 10
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

        results = []

        for item in data.get("results", []):

            results.append({
                "title": item.get("case_name", "Unknown Case"),
                "court": str(item.get("court", "Unknown Court")),
                "date": item.get("date_filed", ""),
                "url": item.get("absolute_url", "")
            })

        return results

    except Exception as e:

        print("COURTLISTENER ERROR:", str(e))

        return []
