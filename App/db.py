from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Database_URL = "postgresql://postgres:1312@localhost:5432/Catalogo"

engine = create_engine(Database_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()