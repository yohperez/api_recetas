# crud.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas


def get_recipes(db: Session, skip: int = 0, limit: int = 100, category_id: int | None = None):
    """
    Obtiene lista de recetas con paginación (skip/limit).
    Opcionalmente filtra por category_id (nivel avanzado: filtro de búsqueda 1:N).
    """
    query = db.query(models.Recipe).offset(skip).limit(limit)
    if category_id:
        query = query.filter(models.Recipe.category_id == category_id)
    return query.all()


def get_recipe(db: Session, recipe_id: int):
    """
    Obtiene una receta por id o None si no existe.
    """
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    """
    Crea una nueva receta en la base de datos.
    El modelo RecipeCreate ya valida que los campos sean correctos.
    """
    # Asegura que la categoría existe antes de crear la receta
    db_category = db.query(models.Category).get(recipe.category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Construye el modelo Recipe con los datos validados
    db_recipe = models.Recipe(
        title=recipe.title,
        description=recipe.description,
        instructions=recipe.instructions,
        cooking_time=recipe.cooking_time,
        prep_time=recipe.prep_time,
        servings=recipe.servings,
        category_id=recipe.category_id,
    )
    # Añade a la sesión y guarda en la base de datos
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)  # Vuelve a cargar el objeto con id y campos generados
    return db_recipe


def update_recipe(db: Session, recipe_id: int, recipe: schemas.RecipeUpdate):
    """
    Actualiza una receta existente.
    Devuelve la receta actualizada o lanza 404 si no existe.
    """
    db_recipe = get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    # Actualiza solo los campos que se puedan cambiar
    db_recipe.title = recipe.title
    db_recipe.description = recipe.description
    db_recipe.instructions = recipe.instructions
    db_recipe.cooking_time = recipe.cooking_time
    db_recipe.prep_time = recipe.prep_time
    db_recipe.servings = recipe.servings
    db_recipe.category_id = recipe.category_id

    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def delete_recipe(db: Session, recipe_id: int):
    """
    Borra una receta por id.
    Si no existe, lanza 404.
    """
    db_recipe = get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    db.delete(db_recipe)
    db.commit()


# (Opcional) Ejemplo de función auxiliar para categorías

def get_categories(db: Session):
    """
    Lista todas las categorías.
    Útil si luego quieres endpoints tipo /api/v1/categories.
    """
    return db.query(models.Category).all()