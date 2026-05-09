from backend.database import SessionLocal, Lawsuit
from backend.court_listener import fetch_latest_cases

def run_daily_scan():
    db = SessionLocal()

    try:
        cases = fetch_latest_cases()

        print("\n=== AI RADAR SCAN START ===")
        print("Fetched:", len(cases))

        if not cases:
            print("NO DATA FROM SOURCES")
            return 0

        inserted = 0
        skipped = 0

        for case in cases:
            try:
                if not isinstance(case, dict):
                    skipped += 1
                    continue

                title = case.get("title") or "Unknown Case"
                court = case.get("court") or "Unknown"
                filed_date = case.get("filed_date") or case.get("date") or ""
                url = case.get("url") or ""
                summary = case.get("summary") or ""
                category = case.get("category") or "general"
                source = case.get("source") or "courtlistener"

                # must have URL
                if not url:
                    skipped += 1
                    continue

                # duplicate protection
                exists = db.query(Lawsuit).filter(Lawsuit.url == url).first()
                if exists:
                    skipped += 1
                    continue

                db.add(Lawsuit(
                    title=title,
                    court=court,
                    filed_date=filed_date,
                    summary=summary,
                    url=url,
                    category=category,
                    source=source
                ))

                inserted += 1

            except Exception as e:
                print("INSERT ERROR:", e)
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
