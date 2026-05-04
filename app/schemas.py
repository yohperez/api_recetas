from pydantic import BaseModel, ConfigDict, Field

class RecipeBase(BaseModel):
    title: str = Field(..., example="Tortilla de Patatas")
    description: str | None = Field(None, example="Receta clásica española")
    instructions: str = Field(..., example="Freír patatas, mezclar con huevo...")
    cooking_time: int = Field(..., gt=0, example=20)

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
