import random

import httpx
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/meals", tags=["TheMealDB (API Externa)"])

BASE_URL = "https://www.themealdb.com/api/json/v1/1"
TIMEOUT = httpx.Timeout(30.0, connect=15.0)


async def _fetch(path: str, params: dict) -> dict:
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/{path}", params=params)
            response.raise_for_status()
        return response.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="API externa indisponivel (timeout)")
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Erro ao acessar API externa")


def _parse_ingredients(meal: dict) -> list[dict]:
    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}", "")
        measure = meal.get(f"strMeasure{i}", "")
        if ingredient and ingredient.strip():
            ingredients.append(
                {"ingredient": ingredient.strip(), "measure": (measure or "").strip()}
            )
    return ingredients


def _format_meal(meal: dict) -> dict:
    return {
        "id": meal.get("idMeal"),
        "name": meal.get("strMeal"),
        "category": meal.get("strCategory"),
        "area": meal.get("strArea"),
        "instructions": meal.get("strInstructions"),
        "image_url": meal.get("strMealThumb"),
        "tags": meal.get("strTags"),
        "youtube": meal.get("strYoutube"),
        "ingredients": _parse_ingredients(meal),
    }


@router.get("/search")
async def search_meals(q: str = Query(..., description="Termo de busca")):
    data = await _fetch("search.php", {"s": q})
    meals = data.get("meals") or []
    return {"results": [_format_meal(m) for m in meals], "count": len(meals)}


@router.get("/categories")
async def list_categories():
    data = await _fetch("categories.php", {})
    categories = data.get("categories") or []
    return {
        "categories": [
            {
                "id": c["idCategory"],
                "name": c["strCategory"],
                "image_url": c["strCategoryThumb"],
                "description": c["strCategoryDescription"],
            }
            for c in categories
        ]
    }


@router.get("/filter")
async def filter_by_category(
    category: str = Query(..., description="Nome da categoria"),
):
    data = await _fetch("filter.php", {"c": category})
    meals = data.get("meals") or []
    return {
        "results": [
            {
                "id": m["idMeal"],
                "name": m["strMeal"],
                "image_url": m["strMealThumb"],
            }
            for m in meals
        ],
        "count": len(meals),
    }


@router.get("/random")
async def random_by_category(
    category: str = Query(..., description="Nome da categoria"),
):
    data = await _fetch("filter.php", {"c": category})
    meals = data.get("meals") or []
    if not meals:
        raise HTTPException(status_code=404, detail="Nenhuma receita encontrada nessa categoria")

    chosen = random.choice(meals)
    detail_data = await _fetch("lookup.php", {"i": chosen["idMeal"]})
    detail = detail_data.get("meals")
    if not detail:
        raise HTTPException(status_code=404, detail="Receita nao encontrada")

    return _format_meal(detail[0])


@router.get("/{meal_id}")
async def get_meal_detail(meal_id: str):
    data = await _fetch("lookup.php", {"i": meal_id})
    meals = data.get("meals")
    if not meals:
        raise HTTPException(status_code=404, detail="Receita nao encontrada")

    return _format_meal(meals[0])
