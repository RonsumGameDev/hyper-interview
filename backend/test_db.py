from backend.models import SessionLocal, Problem
db = SessionLocal()
for p in db.query(Problem).all():
    print(p.id, p.title, p.slots_filled)
db.close()
