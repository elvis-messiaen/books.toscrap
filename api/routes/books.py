# -*- coding: utf-8 -*-
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from api.services.book_service import BookService
from api.models.book import Book

router = APIRouter()
book_service = BookService()


@router.get("/", response_model=List[Book])
def obtenir_tous_les_livres():
    """Recuperer tous les livres."""
    try:
        return book_service.get_all_books()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/{book_id}", response_model=Book)
def obtenir_livre_par_id(book_id: int):
    """Recuperer un livre par son ID."""
    try:
        livre = book_service.get_book_by_id(book_id)
        if not livre:
            raise HTTPException(status_code=404, detail="Livre non trouve")
        return livre
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/category/{category_name}", response_model=List[Book])
def obtenir_livres_par_categorie(category_name: str):
    """Recuperer tous les livres d'une categorie."""
    try:
        return book_service.find_by_category(category_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/search/", response_model=List[Book])
def rechercher_livres(
    titre: Optional[str] = Query(None, description="Rechercher par titre"),
    prix_min: Optional[float] = Query(None, description="Prix minimum"),
    prix_max: Optional[float] = Query(None, description="Prix maximum"),
    note_min: Optional[int] = Query(None, description="Note minimum (1-5)")
):
    """Rechercher des livres avec des filtres."""
    try:
        tous_les_livres = book_service.get_all_books()
        resultats = tous_les_livres

        if titre:
            resultats = [livre for livre in resultats
                        if titre.lower() in livre.title.lower()]

        if prix_min is not None:
            resultats = [livre for livre in resultats
                        if livre.prix_numerique >= prix_min]

        if prix_max is not None:
            resultats = [livre for livre in resultats
                        if livre.prix_numerique <= prix_max]

        if note_min is not None:
            resultats = [livre for livre in resultats
                        if livre.note_etoiles_nombre >= note_min]

        return resultats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")