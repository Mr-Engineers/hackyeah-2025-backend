from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRESQL_URI = f"postgresql+psycopg2://postgres:{PASSWORD}@db.xhduiiqjmhvhzcqkvkya.supabase.co:5432/postgres?sslmode=require"

engine = create_engine(POSTGRESQL_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()