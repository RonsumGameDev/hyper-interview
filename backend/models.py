from sqlalchemy import Column, Integer, String, ForeignKey, Text, create_engine, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    teams = relationship("Team", back_populates="problem", cascade="all, delete-orphan")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    leader_name = Column(String(100), nullable=False)
    contact = Column(String(100), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=True)
    
    problem = relationship("Problem", back_populates="teams")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    
    __table_args__ = (UniqueConstraint("name", name="uq_team_name"),)

class TeamMember(Base):
    __tablename__ = "team_members"
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    name = Column(String(100), nullable=False)
    team = relationship("Team", back_populates="members")

DATABASE_URL = "sqlite:///./hackathon.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
