# models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base


# ----------------- 1:N: Categoría → Recetas -----------------
# Una categoría puede tener muchas recetas, pero cada receta solo tiene una categoría.
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(50),
        unique=True,  # Evita duplicados de nombres de categoría
        index=True,   # Mejora rendimiento en búsquedas/filtros
    )

    # Relación inversa: category.recipes -> lista de recetas de esa categoría
    # back_populates: enlaza con el campo "category" de Recipe
    recipes = relationship(
        "Recipe",
        back_populates="category",
        cascade="all, delete-orphan"  # Si se borra la categoría, se borran sus recetas
    )


# ----------------- Modelo principal: Recipe -----------------
class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(
        String(100),
        index=True,     # Útil para búsquedas y ordenaciones por título
    )
    description = Column(Text)
    instructions = Column(Text)
    cooking_time = Column(Integer, comment="Tiempo de cocción en minutos")
    prep_time = Column(
        Integer,        # Tiempo de preparación, opcional
        nullable=True,
    )
    servings = Column(
        Integer,        # Número de raciones, opcional
        nullable=True,
    )

    # ----------------- Relación 1:N -----------------
    # Clave foránea que apunta a categories.id
    category_id = Column(
        Integer,
        ForeignKey("categories.id"),  # 1:N con Category
        nullable=False,
    )

    # Campo de trazabilidad (útil para GDPR/auditoría)
    created_at = Column(
        DateTime,
        default=datetime.utcnow  # Marca de tiempo de creación
    )

    # Relación directa: recipe.category -> categoría de la receta
    # back_populates: enlaza con "recipes" de Category
    category = relationship(
        "Category",
        back_populates="recipes"
    )