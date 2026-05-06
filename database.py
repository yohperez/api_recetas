"""
database.py - Configuración de la Base de Datos

Este archivo gestiona todo lo relacionado con la conexión a PostgreSQL:
1. Crea el "motor" (engine) asíncrono que gestiona las conexiones.
2. Crea la "fábrica de sesiones" para interactuar con la BD.
3. Define la función `get_db`, que FastAPI usará como dependencia.

Conceptos Clave:
-----------------
- **Engine**: Es el punto de conexión con la BD. Lo creamos una sola vez
  para toda la aplicación. Gestiona un "pool" de conexiones internamente.

- **Session (AsyncSession)**: Es una "unidad de trabajo". Cada petición HTTP
  obtiene su propia sesión, usa la BD, y luego la sesión se cierra.
  Piensa en ella como una "conversación" temporal con la base de datos.

- **Base**: Clase base de SQLAlchemy de la que heredarán todos nuestros modelos.
  SQLAlchemy la usa para saber qué tablas debe crear/gestionar.
"""

import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# --- Cargar Variables de Entorno ---
load_dotenv()

# --- URL de Conexión ---
# En producción, esto vendría de una variable de entorno segura.
# El driver `asyncpg` es el adaptador asíncrono para PostgreSQL.
# Formato: postgresql+asyncpg://usuario:contraseña@host:puerto/nombre_bd
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/saborscript_db"
)

# --- Motor Asíncrono ---
# `create_async_engine` crea el motor que gestiona el pool de conexiones.
# `echo=True` hace que SQLAlchemy imprima las queries SQL en la consola (útil para debugging).
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    pool_size=10,        # Número de conexiones en el pool
    max_overflow=20,     # Conexiones extras si es necesario
)

# --- Fábrica de Sesiones ---
# `async_sessionmaker` crea una "plantilla" para generar nuevas sesiones.
# - `expire_on_commit=False`: Evita que los objetos se "olviden" después de un commit,
#   lo que nos permite seguir leyendo sus atributos sin hacer otra consulta a la BD.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# --- Clase Base para Modelos ---
class Base(DeclarativeBase):
    """
    Todos los modelos de la BD heredarán de esta clase.
    SQLAlchemy la usa internamente para registrar las tablas.
    """
    pass


# --- Dependencia de Base de Datos ---
async def get_db():
    """
    Generador asíncrono que provee una sesión de BD a los endpoints.

    Uso con FastAPI:
        async def mi_endpoint(db: AsyncSession = Depends(get_db)):
            ...

    ¿Cómo funciona el `yield`?
    --------------------------
    - El código ANTES del `yield` se ejecuta al inicio de cada petición:
      crea y entrega la sesión.
    - El código DESPUÉS del `yield` se ejecuta al final (en el bloque `finally`):
      cierra la sesión, liberando la conexión de vuelta al pool.
    - Esto garantiza que la sesión siempre se cierre, incluso si ocurre un error.
    """
    async with AsyncSessionLocal() as session:
        yield session  # Entrega la sesión al endpoint
        # Al salir del `async with`, la sesión se cierra automáticamente
