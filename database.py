from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class JobModel(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    job_id = Column(String)
    location = Column(String)
    start_time = Column(DateTime)
    duration_hours = Column(Integer)
    priority = Column(Integer)
    outdoor = Column(Boolean)

def init_db():
    engine = create_engine('sqlite:///data/scheduler.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
