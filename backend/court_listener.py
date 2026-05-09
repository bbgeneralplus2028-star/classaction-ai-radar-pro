import requests

def fetch_latest_cases():
    try:
        url = "https://www.courtlistener.com/api/rest/v3/dockets/"

        response = requests.get(url)

        print("STATUS:", response.status_code)

        data = response.json()

        print("DATA:", data)

        results = []

        for item in data.get("results", []):
            results.append({
                "title": item.get("case_name", "Unknown"),
                "court": str(item.get("court", "Unknown")),
                "date": item.get("date_filed", ""),
                "url": item.get("absolute_url", "")
            })

        print("RESULTS:", results)

        return results

    except Exception as e:
        print("ERROR:", str(e))
        return []
