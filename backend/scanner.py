from backend.database import SessionLocal, Lawsuit
from backend.court_listener import fetch_latest_cases

def run_daily_scan():
    db = SessionLocal()

    try:
        cases = fetch_latest_cases()

        print("\n=== RAW INPUT ===")
        print(f"Total fetched: {len(cases)}")

        if not cases:
            print("NO DATA FROM ANY SOURCE")
            return 0

        inserted = 0
        skipped = 0

        for case in cases:
            try:
                if not isinstance(case, dict):
                    continue

                title = case.get("title") or "Unknown Case"
                court = case.get("court") or "Unknown"
                date = case.get("date") or ""
                url = case.get("url") or ""

                if not url:
                    skipped += 1
                    continue

                # prevent duplicates
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
                print("ERROR:", e)
                skipped += 1

        db.commit()

        print("\n=== SCAN RESULT ===")
        print("Inserted:", inserted)
        print("Skipped:", skipped)

        return inserted

    except Exception as e:
        db.rollback()
        print("SCAN FAILED:", e)
        return 0

    finally:
        db.close()
