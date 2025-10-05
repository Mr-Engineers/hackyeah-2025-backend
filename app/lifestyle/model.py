from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import JSONB
from ..database import Base

class LifestyleAction(Base):
    __tablename__ = "lifestyle_actions"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    cost = Column(Float)

    effects = Column(JSONB)
    requirements = Column(JSONB, default={})


    