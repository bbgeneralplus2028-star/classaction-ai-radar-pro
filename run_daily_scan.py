from backend.database import SessionLocal, Lawsuit
from backend.court_listener import fetch_latest_cases

def run_daily_scan():
    db = SessionLocal()

    try:
        cases = fetch_latest_cases()

        print("RAW CASES OUTPUT:", cases)
        print("TYPE:", type(cases))

        if not cases:
            print("NO CASES RETURNED FROM SOURCE")
            return 0

        if not isinstance(cases, list):
            print("INVALID CASE FORMAT (NOT A LIST)")
            return 0

        inserted = 0

        for case in cases:
            try:
                if not isinstance(case, dict):
                    print("SKIPPING NON-DICT CASE:", case)
                    continue

                title = case.get("title") or "Unknown"
                court = case.get("court") or "Unknown"
                date = case.get("date") or ""
                url = case.get("url") or ""

                # Skip completely empty records
                if title == "Unknown" and not url:
                    print("SKIPPING EMPTY CASE:", case)
                    continue

                lawsuit = Lawsuit(
                    title=str(title),
                    court=str(court),
                    date=str(date),
                    url=str(url)
                )

                db.add(lawsuit)
                inserted += 1

            except Exception as inner:
                print("INSERT ERROR:", inner)

        # Only commit if something was added
        if inserted > 0:
            db.commit()
        else:
            db.rollback()

        print("TOTAL INSERTED:", inserted)
        return inserted

    except Exception as e:
        db.rollback()
        print("SCAN FAILED:", e)
        return 0

    finally:
        db.close()
