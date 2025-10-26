from models import Base, engine, SessionLocal, Problem, Team

def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Problem).count() == 0:
            samples = [
                Problem(title="AI for Water Management", description="Build AI models for efficient water usage."),
                Problem(title="Smart Waste Segregation", description="IoT system for automated waste sorting."),
                Problem(title="Green Energy Optimizer", description="Optimize solar/wind energy consumption using ML."),
            ]
            db.add_all(samples)
            db.commit()
            print("Sample problems added.")
        else:
            print("Problems already present.")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
