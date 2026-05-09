import requests

def fetch_latest_cases():
    try:
        url = "https://example.com/api/cases"  # replace with real source

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        print("FETCH RAW RESPONSE:", data)

        # Normalize structure
        if isinstance(data, dict):
            data = data.get("results") or data.get("data") or []

        if not isinstance(data, list):
            return []

        cleaned = []

        for item in data:
            if not isinstance(item, dict):
                continue

            cleaned.append({
                "title": item.get("title"),
                "court": item.get("court"),
                "date": item.get("date"),
                "url": item.get("url")
            })

        return cleaned

    except Exception as e:
        print("FETCH ERROR:", e)
        return []
