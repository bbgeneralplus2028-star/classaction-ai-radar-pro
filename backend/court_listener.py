import requests

def fetch_latest_cases():

    url = "https://www.courtlistener.com/api/rest/v3/dockets/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        print("STATUS CODE:", response.status_code)

        data = response.json()

        print("API RESPONSE:", data)

        cases = []

        results = data.get("results", [])

        for item in results:

            title = item.get("case_name")

            if not title:
                continue

            cases.append({
                "title": title,
                "court": str(item.get("court")),
                "date": item.get("date_filed"),
                "url": item.get("absolute_url")
            })

        print("TOTAL CASES:", len(cases))

        return cases

    except Exception as e:

        print("COURTLISTENER ERROR:", str(e))

        return []
