# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# En desarrollo puedes usar SQLite
# En producción eso cambiaría (por ejemplo a PostgreSQL)

# Opción 1: SQLite
DATABASE_URL = "sqlite:///./recetas.db"  # Fichero en la raíz del proyecto

# Opción 2: PostgreSQL (para nivel experto con Docker)
# DATABASE_URL = "postgresql://user:password@db:5432/recetas_db"

engine = create_engine(
    DATABASE_URL,
    # Para SQLite, necesario para que funcione bien en varios hilos
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ------------------- Cómo se usa en tu app -------------------
# - En main.py: Base.metadata.create_all(bind=engine)
# - En routers: get_db() → SessionLocal()