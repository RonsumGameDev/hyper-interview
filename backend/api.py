from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from .models import SessionLocal, Team, TeamMember, Problem, Base, engine

app = FastAPI(title="Hackathon Backend")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TeamRegisterRequest(BaseModel):
    team_name: str
    leader_name: str
    contact: str
    member_names: List[str]

class ProblemSelectRequest(BaseModel):
    team_id: int
    problem_statement: str

@app.get("/problems")
def get_problems(db: Session = Depends(get_db)):
    problems = db.query(Problem).all()
    result = []
    for p in problems:
        count = db.query(Team).filter(Team.problem_id == p.id).count()
        result.append({
            "title": p.title,
            "slots_filled": count
        })
    return result

@app.post("/register")
def register_team(req: TeamRegisterRequest, db: Session = Depends(get_db)):

    team_name = req.team_name.strip()
    leader_name = req.leader_name.strip()
    contact = req.contact.strip()
    member_names = [name.strip() for name in req.member_names if name.strip()]

    if not team_name:
        raise HTTPException(status_code=400, detail="Team name required")
    if not leader_name:
        raise HTTPException(status_code=400, detail="Team leader name required")
    if not contact:
        raise HTTPException(status_code=400, detail="Contact required")
    if len(member_names) == 0:
        raise HTTPException(status_code=400, detail="At least one team member required")
    if len(member_names) > 4:
        raise HTTPException(status_code=400, detail="Maximum 4 team members allowed")

    if db.query(Team).filter(Team.name == team_name).first():
        raise HTTPException(status_code=400, detail="Team name already exists")

    team = Team(name=team_name, leader_name=leader_name, contact=contact)
    db.add(team)
    db.commit()
    db.refresh(team)

    for member_name in member_names:
        db.add(TeamMember(team_id=team.id, name=member_name))
    db.commit()

    return {"message": f"Team '{team.name}' registered", "team_id": team.id}

@app.post("/select_problem")
def select_problem(req: ProblemSelectRequest, db: Session = Depends(get_db)):
    team_id = req.team_id
    problem_title = req.problem_statement.strip()

    if not team_id or not problem_title:
        raise HTTPException(status_code=400, detail="team_id and problem_statement required")

    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if team.problem_id:
        raise HTTPException(status_code=400, detail="Problem already selected, cannot change")

    problem = db.query(Problem).filter(Problem.title == problem_title).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    count = db.query(Team).filter(Team.problem_id == problem.id).count()
    if count >= 5:
        raise HTTPException(status_code=400, detail="Problem is full")

    team.problem_id = problem.id
    db.commit()
    return {"message": f"Problem '{problem.title}' selected for team '{team.name}'"}
