from backend.database import SessionLocal, Lawsuit
from backend.court_listener import fetch_latest_cases

def run_daily_scan():
    db = SessionLocal()

    try:
        cases = fetch_latest_cases()

        print("CASES:", cases)

        inserted = 0

        for case in cases or []:
            try:
                lawsuit = Lawsuit(
                    title=str(case.get("title", "Unknown")),
                    court=str(case.get("court", "Unknown")),
                    date=str(case.get("date", "")),
                    url=str(case.get("url", ""))
                )

                db.add(lawsuit)
                inserted += 1

            except Exception as inner:
                print("INSERT ERROR:", inner)

        db.commit()
        return inserted

    except Exception as e:
        db.rollback()
        print("SCAN FAILED:", e)
        return 0

    finally:
        db.close()
