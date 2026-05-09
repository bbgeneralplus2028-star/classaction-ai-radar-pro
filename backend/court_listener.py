import requests

def fetch_courtlistener():
    try:
        url = "https://www.courtlistener.com/api/rest/v4/opinions/"
        r = requests.get(url, params={"page_size": 20}, timeout=15)

        if r.status_code != 200:
            return []

        data = r.json().get("results", [])

        return [
            {
                "title": x.get("caseName") or "Unknown Case",
                "court": str(x.get("court") or "Unknown"),
                "date": x.get("date_created") or "",
                "url": x.get("absolute_url") or ""
            }
            for x in data
        ]
    except:
        return []


def fetch_google_law_news():
    try:
        url = "https://news.google.com/rss/search?q=class+action+lawsuit"
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return []

        # simple fallback parsing (no XML lib dependency)
        items = r.text.split("<item>")[1:11]

        results = []

        for item in items:
            try:
                title = item.split("<title>")[1].split("</title>")[0]
                link = item.split("<link>")[1].split("</link>")[0]

                results.append({
                    "title": title,
                    "court": "News Source",
                    "date": "",
                    "url": link
                })
            except:
                continue

        return results
    except:
        return []


def fetch_latest_cases():
    """
    MASTER AGGREGATOR
    """
    results = []

    results.extend(fetch_courtlistener())
    results.extend(fetch_google_law_news())

    return results
