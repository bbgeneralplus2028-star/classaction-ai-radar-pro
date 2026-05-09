from backend.database import SessionLocal, Lawsuit
from backend.court_listener import fetch_latest_cases

def run_daily_scan():
    db = SessionLocal()

    try:
        cases = fetch_latest_cases()

        print("\n=== RAW CASES RECEIVED ===")
        print(cases)

        if not cases:
            print("NO CASES RETURNED FROM SOURCE")
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

                # Skip invalid entries
                if not url:
                    print(f"[SKIP {i}] NO URL")
                    continue

                # Prevent duplicates
                exists = db.query(Lawsuit).filter(Lawsuit.url == url).first()
                if exists:
                    print(f"[SKIP {i}] DUPLICATE")
                    continue

                db.add(Lawsuit(
                    title=title,
                    court=court,
                    date=date,
                    url=url
                ))

                inserted += 1

            except Exception as e:
                print(f"[ERROR {i}]", e)

        db.commit()

        print("\n=== SCAN COMPLETE ===")
        print("INSERTED:", inserted)

        return inserted

    except Exception as e:
        db.rollback()
        print("SCAN FAILED:", e)
        return 0

    finally:
        db.close()
