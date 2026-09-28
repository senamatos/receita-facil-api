from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import recipes, meals

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Receita Fácil API",
    description="API para gerenciamento de receitas favoritas com integracao ao TheMealDB",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipes.router)
app.include_router(meals.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "Receita Fácil API"}
