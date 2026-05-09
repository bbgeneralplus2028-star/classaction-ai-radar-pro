from backend.database import SessionLocal, Lawsuit
from backend.court_listener import fetch_latest_cases

def run_daily_scan():
    db = SessionLocal()

    try:
        cases = fetch_latest_cases()

        print("\n=== RAW CASES ===")
        print(cases)
        print("TYPE:", type(cases), "\n")

        if not cases:
            print("NO CASES RETURNED")
            return 0

        if not isinstance(cases, list):
            print("INVALID CASE FORMAT")
            return 0

        inserted = 0
        skipped = 0

        for i, case in enumerate(cases):
            try:
                if not isinstance(case, dict):
                    print(f"[SKIP {i}] NOT A DICT:", case)
                    skipped += 1
                    continue

                title = case.get("title") or "Unknown"
                court = case.get("court") or "Unknown"
                date = case.get("date") or ""
                url = case.get("url") or ""

                # Skip useless records
                if title == "Unknown" and not url:
                    print(f"[SKIP {i}] EMPTY CASE:", case)
                    skipped += 1
                    continue

                # Prevent duplicates (basic safety)
                exists = db.query(Lawsuit).filter(Lawsuit.url == url).first()
                if exists:
                    print(f"[SKIP {i}] DUPLICATE:", url)
                    skipped += 1
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
                print(f"[ERROR {i}] INSERT FAILED:", inner)
                skipped += 1

        if inserted > 0:
            db.commit()
        else:
            db.rollback()

        print("\n=== SCAN RESULT ===")
        print("INSERTED:", inserted)
        print("SKIPPED:", skipped)

        return inserted

    except Exception as e:
        db.rollback()
        print("SCAN FAILED HARD:", e)
        return 0

    finally:
        db.close()
