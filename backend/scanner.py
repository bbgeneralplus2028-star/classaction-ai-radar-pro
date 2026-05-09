import requests
from ai_summary import summarize_lawsuit
from database import SessionLocal, Lawsuit
from notification_engine import create_notification

create_notification(
    title="New Class Action Detected",
    message=summary,
    lawsuit_id=lawsuit.id
)
COURTLISTENER_URL = "https://www.courtlistener.com/api/rest/v3/dockets/"

def run_daily_scan():
    db = SessionLocal()
    data = requests.get(COURTLISTENER_URL).json()

    for item in data.get("results", [])[:15]:

        title = item.get("case_name", "Unknown Case")
        court = item.get("court", "")
        date = item.get("date_filed", "")
        url = item.get("absolute_url", "")

        summary = summarize_lawsuit(title)

        exists = db.query(Lawsuit).filter(Lawsuit.title == title).first()
        if exists:
            continue

        lawsuit = Lawsuit(
            title=title,
            court=court,
            filed_date=date,
            summary=summary,
            url=f"https://courtlistener.com{url}"
        )

        db.add(lawsuit)

    db.commit()
