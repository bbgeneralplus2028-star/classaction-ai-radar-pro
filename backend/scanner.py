from backend.database import SessionLocal, Lawsuit
from backend.court_listener import fetch_latest_cases

def run_daily_scan():
    db = SessionLocal()

    try:
        cases = fetch_latest_cases()

        print("\n=== RAW CASES ===")
        print(cases)
        print("TYPE:", type(cases))

        if not cases or not isinstance(cases, list):
            print("NO VALID CASES FOUND")
            return 0

        inserted = 0

        for i, case in enumerate(cases):
            try:
                if not isinstance(case, dict):
                    continue

                title = case.get("title") or "Unknown Case"
                court = case.get("court") or "Unknown"
                date = case.get("date") or ""
                url = case.get("url") or ""

                # Skip useless entries
                if title == "Unknown Case" and not url:
                    continue

                # Prevent duplicates
                exists = db.query(Lawsuit).filter(Lawsuit.url == url).first()
                if exists:
                    continue

                db.add(Lawsuit(
                    title=title,
                    court=court,
                    date=date,
                    url=url
                ))

                inserted += 1

            except Exception as e:
                print(f"INSERT ERROR {i}:", e)

        if inserted > 0:
            db.commit()
        else:
            db.rollback()

        print("INSERTED TOTAL:", inserted)

        return inserted

    except Exception as e:
        db.rollback()
        print("SCAN FAILED:", e)
        return 0

    finally:
        db.close()
