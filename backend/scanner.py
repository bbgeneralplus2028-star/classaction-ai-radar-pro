from backend.database import SessionLocal, Lawsuit
from backend.court_listener import fetch_latest_cases

def run_daily_scan():
    db = SessionLocal()
    cases = fetch_latest_cases()

    inserted = 0

    for case in cases:
        db.add(Lawsuit(
            title=case.get("title"),
            court=case.get("court"),
            date=case.get("date"),
            url=case.get("url")
        ))
        inserted += 1

    db.commit()
    db.close()

    return inserted
