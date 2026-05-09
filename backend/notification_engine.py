from database import SessionLocal, Notification
from datetime import datetime

def create_notification(title, message, lawsuit_id):

    db = SessionLocal()

    note = Notification(
        title=title,
        message=message,
        type="lawsuit_alert",
        created_at=str(datetime.now()),
        lawsuit_id=lawsuit_id
    )

    db.add(note)
    db.commit()
