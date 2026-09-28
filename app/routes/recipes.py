import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Recipe
from app.schemas import RecipeCreate, RecipeUpdate, RecipeResponse, PaginatedResponse

router = APIRouter(prefix="/recipes", tags=["Receitas Favoritas"])


@router.get("/", response_model=PaginatedResponse)
def list_recipes(
    page: int = Query(1, ge=1, description="Numero da pagina"),
    per_page: int = Query(10, ge=1, le=50, description="Itens por pagina"),
    category: str | None = Query(None, description="Filtrar por categoria"),
    area: str | None = Query(None, description="Filtrar por regiao"),
    search: str | None = Query(None, description="Buscar por nome"),
    sort_by: str = Query("created_at", description="Ordenar por campo"),
    order: str = Query("desc", description="asc ou desc"),
    db: Session = Depends(get_db),
):
    query = db.query(Recipe)

    if category:
        query = query.filter(Recipe.category == category)
    if area:
        query = query.filter(Recipe.area == area)
    if search:
        query = query.filter(Recipe.name.ilike(f"%{search}%"))

    sort_column = getattr(Recipe, sort_by, Recipe.created_at)
    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    total = query.count()
    pages = math.ceil(total / per_page) if total > 0 else 1
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return PaginatedResponse(
        items=items, total=total, page=page, per_page=per_page, pages=pages
    )


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Receita nao encontrada")
    return recipe


@router.post("/", response_model=RecipeResponse, status_code=201)
def create_recipe(data: RecipeCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(Recipe).filter(Recipe.external_id == data.external_id).first()
    )
    if existing:
        raise HTTPException(
            status_code=409, detail="Receita ja esta nos favoritos"
        )

    recipe = Recipe(**data.model_dump())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int, data: RecipeUpdate, db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Receita nao encontrada")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(recipe, field, value)

    db.commit()
    db.refresh(recipe)
    return recipe


@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Receita nao encontrada")

    db.delete(recipe)
    db.commit()
