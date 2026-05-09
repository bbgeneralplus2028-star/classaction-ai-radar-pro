from backend.database import SessionLocal, Lawsuit
from backend.court_listener import fetch_latest_cases

def run_daily_scan():
    db = SessionLocal()
    inserted = 0

    try:
        cases = fetch_latest_cases()

        if not cases:
            return 0

        for case in cases:
            # skip bad records safely
            if not isinstance(case, dict):
                continue

            title = case.get("title")
            court = case.get("court")
            date = case.get("date")
            url = case.get("url")

            # only insert if at least title exists
            if not title:
                continue

            lawsuit = Lawsuit(
                title=title,
                court=court,
                date=date,
                url=url
            )

            db.add(lawsuit)
            inserted += 1

        db.commit()
        return inserted

    except Exception as e:
        db.rollback()
        print("run_daily_scan error:", str(e))
        return 0

    finally:
        db.close()
