"""
Module principal de l'API FastAPI pour les données de scraping de livres.
"""

from fastapi import FastAPI

app = FastAPI(title="Books to Scrape API")

@app.get("/")
def accueil():
    """
    Page d'accueil de l'API.
    """
    return {
        "message": "API Books to Scrape",
        "documentation": "/docs"
    }

@app.get("/books")
def obtenir_livres():
    """
    Récupérer la liste des livres.
    """
    return {"message": "Liste des livres - à implémenter"}

@app.get("/categories")
def obtenir_categories():
    """
    Récupérer la liste des catégories.
    """
    return {"message": "Liste des catégories - à implémenter"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)