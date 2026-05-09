from backend.court_listener import fetch_latest_cases
from backend.database import SessionLocal, Lawsuit

def run_daily_scan():
    db = SessionLocal()

    cases = fetch_latest_cases(limit=25)

    for case in cases:
        if "error" in case:
            continue

        exists = db.query(Lawsuit).filter(Lawsuit.title == case["title"]).first()

        if not exists:
            new_case = Lawsuit(
                title=case["title"],
                court=case["court"],
                filed_date=case["filed_date"],
                summary=case["summary"],
                url=case["url"]
            )
            db.add(new_case)

    db.commit()
    db.close()

    return {"status": "scan complete", "count": len(cases)}
