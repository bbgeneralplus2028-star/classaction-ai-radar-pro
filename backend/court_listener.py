import requests

def fetch_latest_cases():
    url = "https://www.courtlistener.com/api/rest/v3/dockets/"

    params = {
        "page_size": 5
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    results = []

    for item in data.get("results", []):
        results.append({
            "title": item.get("case_name", "Unknown Case"),
            "court": item.get("court", "Unknown Court"),
            "date": item.get("date_filed", ""),
            "url": item.get("absolute_url", "")
        })

    return results
