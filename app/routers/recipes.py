# recipes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from . import schemas, crud
from .database import SessionLocal


router = APIRouter()


def get_db():
    """
    Dependencia: abre una sesión de base de datos para cada request.
    - yield: provee la sesión a la ruta.
    - finally: cierra la sesión tras la respuesta.
    Es el patrón estándar de FastAPI + SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================== CRUD RECIPE ========================

@router.post("/", response_model=schemas.Recipe, status_code=status.HTTP_201_CREATED)
def create_recipe(
    recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db),
):
    """
    Crea una nueva receta.
    - schema: RecipeCreate (valida entrada).
    - status_code 201: recurso creado.
    """
    return crud.create_recipe(db=db, recipe=recipe)


@router.get("/", response_model=List[schemas.Recipe])
def read_recipes(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Obtiene lista de recetas con paginación (skip/limit).
    Opcionalmente filtra por category_id (1:N -> filtro avanzado).
    """
    return crud.get_recipes(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
    )


@router.get("/{recipe_id}", response_model=schemas.Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una receta por id.
    Si no existe, lanza 404 (gestión de errores).
    """
    db_recipe = crud.get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return db_recipe


@router.put("/{recipe_id}", response_model=schemas.Recipe)
def update_recipe(
    recipe_id: int,
    recipe: schemas.RecipeUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualiza una receta existente.
    - schema: RecipeUpdate (valida los nuevos datos).
    - Si la receta no existe: 404.
    """
    return crud.update_recipe(db, recipe_id, recipe)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Borra una receta por id.
    - Devuelve 204 NO CONTENT (sin cuerpo).
    - Si no existe, lanza 404.
    """
    crud.delete_recipe(db, recipe_id)
    return None  # FastAPI responde 204 automáticamente