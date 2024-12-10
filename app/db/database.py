from sqlalchemy import Column, Integer, Float, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session

# FIXME: should not be declared outside of a class scope
Base = declarative_base()

class Database:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        db = self.SessionLocal() 
        try:
            yield db
        finally:
            db.close()
