"""
Module principal de l'API FastAPI pour les données de scraping de livres.
"""

from fastapi import FastAPI
from api.routes import books, categories

# Créer l'application FastAPI
app = FastAPI(
    title="Books to Scrape API",
    description="API REST pour accéder aux données de livres scrapées",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enregistrer les routes
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])


@app.get("/")
def accueil():
    """
    Page d'accueil de l'API avec informations sur les endpoints.
    """
    return {
        "message": "API Books to Scrape",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "books": "/books",
            "categories": "/categories",
            "examples": {
                "all_books": "/books/",
                "book_by_id": "/books/1",
                "books_by_category": "/books/category/Mystery",
                "search_books": "/books/search/?titre=harry&prix_min=10&prix_max=50"
            }
        }
    }


@app.get("/health")
def verifier_sante():
    """
    Endpoint de vérification de l'état de l'API.
    """
    return {"status": "healthy", "service": "books-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)