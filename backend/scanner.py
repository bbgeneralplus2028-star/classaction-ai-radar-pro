from backend.database import SessionLocal, Lawsuit
from backend.court_listener import fetch_latest_cases

def run_daily_scan():
    db = SessionLocal()

    try:
        cases = fetch_latest_cases()

        print("\n=== FETCHED CASES ===")
        print("Count:", len(cases) if cases else 0)

        if not cases:
            print("NO DATA RETURNED")
            return 0

        inserted = 0
        skipped = 0

        for i, case in enumerate(cases):
            try:
                if not isinstance(case, dict):
                    skipped += 1
                    continue

                title = case.get("title") or "Unknown Case"
                court = case.get("court") or "Unknown"
                date = case.get("date") or ""
                url = case.get("url") or ""

                if not url:
                    skipped += 1
                    continue

                # duplicate check
                exists = db.query(Lawsuit).filter(Lawsuit.url == url).first()
                if exists:
                    skipped += 1
                    continue

                db.add(Lawsuit(
                    title=title,
                    court=court,
                    date=date,
                    url=url
                ))

                inserted += 1

            except Exception as e:
                print(f"ERROR {i}:", e)
                skipped += 1

        db.commit()

        print("INSERTED:", inserted)
        print("SKIPPED:", skipped)

        return inserted

    except Exception as e:
        db.rollback()
        print("SCAN FAILED:", e)
        return 0

    finally:
        db.close()
