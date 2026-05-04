from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(Text)
    instructions = Column(Text)
    cooking_time = Column(Integer)  # en minutos
