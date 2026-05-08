# schemas.py
from pydantic import BaseModel
from typing import Optional, List


# ==================== SCHEMAS PARA CATEGORÍA ====================

class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    recipes: List["Recipe"] = []  # Campos relacionados (opcional)

    class Config:
        from_attributes = True  # SQLAlchemy → Pydantic (anterior orm_mode=True)


# ==================== SCHEMAS PARA RECETAS ====================

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    cooking_time: int
    prep_time: Optional[int] = None
    servings: Optional[int] = None
    category_id: int  # FK; la categoría debe existir


class RecipeCreate(RecipeBase):
    # Campos exactamente como en la creación (todos requeridos)
    pass


class RecipeUpdate(RecipeBase):
    # En la actualización, algunos campos pueden ser opcionales
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    cooking_time: Optional[int] = None
    prep_time: Optional[int] = None
    servings: Optional[int] = None
    category_id: Optional[int] = None


class Recipe(RecipeBase):
    id: int
    created_at: Optional[str] = None

    # Añade categoría anidada en la respuesta (opcional, para Swagger)
    category: Optional[Category] = None

    class Config:
        from_attributes = True


# ------------------- Para evitar warning de referencia circular -------------------
# Esto se puede mover a otro fichero más adelante si creces mucho
Category.model_rebuild()

# Hint: con estos schemas, FastAPI valida:
# - Tipos de datos.
# - Campos obligatorios/opcionales.
# - Permite documentar ejemplos automáticos en Swagger.