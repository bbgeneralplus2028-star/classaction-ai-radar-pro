import requests

def fetch_latest_cases():

    try:

        url = "https://www.courtlistener.com/api/rest/v3/dockets/"

        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print("STATUS:", response.status_code)

        raw = response.text

        print("RAW RESPONSE:")
        print(raw)

        data = response.json()

        print("JSON TYPE:", type(data))

        print("JSON KEYS:", data.keys())

        results = data.get("results", [])

        print("RESULT COUNT:", len(results))

        lawsuits = []

        for item in results:

            lawsuits.append({
                "title": str(item),
                "court": "Unknown",
                "date": "",
                "url": ""
            })

        return lawsuits

    except Exception as e:

        print("FULL ERROR:", str(e))

        return []
