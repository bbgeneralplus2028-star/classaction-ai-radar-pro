from backend.database import SessionLocal, Lawsuit
from backend.court_listener import fetch_latest_cases

def run_daily_scan():
    db = SessionLocal()

    try:
        cases = fetch_latest_cases()

        inserted = 0

        for case in cases:

            # Prevent duplicates
            existing = db.query(Lawsuit).filter(
                Lawsuit.url == case.get("url")
            ).first()

            if existing:
                continue

            lawsuit = Lawsuit(
                title=case.get("title"),
                court=case.get("court"),
                date=case.get("date"),
                url=case.get("url")
            )

            db.add(lawsuit)

            inserted += 1

        db.commit()

        return inserted

    except Exception as e:
        print("SCAN ERROR:", str(e))
        return 0

    finally:
        db.close()
