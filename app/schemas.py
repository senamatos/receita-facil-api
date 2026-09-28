from pydantic import BaseModel, Field
from datetime import datetime


class RecipeCreate(BaseModel):
    external_id: str
    name: str
    category: str | None = None
    area: str | None = None
    instructions: str | None = None
    image_url: str | None = None
    ingredients: str | None = None
    notes: str | None = None
    rating: float | None = Field(None, ge=0, le=5)


class RecipeUpdate(BaseModel):
    notes: str | None = None
    rating: float | None = Field(None, ge=0, le=5)


class RecipeResponse(BaseModel):
    id: int
    external_id: str
    name: str
    category: str | None
    area: str | None
    instructions: str | None
    image_url: str | None
    ingredients: str | None
    notes: str | None
    rating: float | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    items: list[RecipeResponse]
    total: int
    page: int
    per_page: int
    pages: int
