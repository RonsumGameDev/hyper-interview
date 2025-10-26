from models import SessionLocal, Team

db = SessionLocal()
try:
    deleted = db.query(Team).delete()
    db.commit()
    print(f"Deleted {deleted} teams from the database.")
finally:
    db.close()
