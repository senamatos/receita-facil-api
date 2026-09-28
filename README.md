# Receita Fácil API

API REST para gerenciamento de receitas favoritas, com integração ao serviço externo [TheMealDB](https://www.themealdb.com/api.php). Desenvolvida com **FastAPI** e **SQLite**.

## Arquitetura

Este componente faz parte de um sistema de três módulos:

- **Frontend React** — Interface do usuário
- **API Backend (este repositório)** — Gerencia favoritos e consome a API externa
- **TheMealDB** — API externa pública de receitas

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy (ORM)
- SQLite (persistência)
- httpx (cliente HTTP assíncrono)
- Docker

## Rotas da API

### Receitas Favoritas (`/recipes`)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/recipes/` | Listar favoritos (com paginação, filtros e ordenação) |
| `GET` | `/recipes/{id}` | Obter detalhes de um favorito |
| `POST` | `/recipes/` | Adicionar receita aos favoritos |
| `PUT` | `/recipes/{id}` | Atualizar notas e avaliação |
| `DELETE` | `/recipes/{id}` | Remover dos favoritos |

### TheMealDB (`/meals`)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/meals/search?q=` | Buscar receitas por nome |
| `GET` | `/meals/categories` | Listar categorias |
| `GET` | `/meals/filter?category=` | Filtrar receitas por categoria |
| `GET` | `/meals/{meal_id}` | Detalhes de uma receita |

### Funcionalidades extras

- **Paginação**: parâmetros `page` e `per_page`
- **Filtros**: por `category`, `area` e `search` (nome)
- **Ordenação**: parâmetros `sort_by` e `order` (asc/desc)

## Instalação Local

### Pré-requisitos

- Python 3.12+
- pip

### Passos

```bash
# Clonar o repositório
git clone https://github.com/senamatos/receita-facil-api.git
cd receita-facil-api

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor
uvicorn app.main:app --reload
```

O servidor estará disponível em `http://localhost:8000`.

A documentação interativa (Swagger) pode ser acessada em `http://localhost:8000/docs`.

## Execução com Docker

```bash
# Build da imagem
docker build -t recipe-hub-api .

# Executar o container
docker run -p 8000:8000 recipe-hub-api
```

## Estrutura do Projeto

```
recipe-hub-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # Ponto de entrada da aplicação
│   ├── database.py      # Configuração do banco de dados
│   ├── models.py        # Modelos SQLAlchemy
│   ├── schemas.py       # Schemas Pydantic
│   └── routes/
│       ├── __init__.py
│       ├── recipes.py   # CRUD de receitas favoritas
│       └── meals.py     # Integração com TheMealDB
├── requirements.txt
├── Dockerfile
└── README.md
```
