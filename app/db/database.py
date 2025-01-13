from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


class Database:
    def __init__(self, db_url: str):
        self.base = declarative_base()
        self._engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self._session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

    def create_tables(self):
        self.base.metadata.create_all(bind=self._engine)

    def get_session(self):
        db = self._session_local()
        try:
            yield db
        finally:
            db.close()
