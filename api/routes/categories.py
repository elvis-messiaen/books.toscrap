# -*- coding: utf-8 -*-
from typing import List
from fastapi import APIRouter, HTTPException
from api.services.category_service import CategoryService
from api.services.book_service import BookService
from api.models.prix_moyen_categorie import PrixMoyenCategorie
from api.models.top_categorie import TopCategorie

router = APIRouter()
category_service = CategoryService()
book_service = BookService()


@router.get("/")
def obtenir_toutes_les_categories():
    """Recuperer toutes les categories."""
    try:
        return category_service.get_all_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/{category_id}")
def obtenir_categorie_par_id(category_id: int):
    """Recuperer une categorie par son ID."""
    try:
        categorie = category_service.get_category_by_id(category_id)
        if not categorie:
            raise HTTPException(status_code=404, detail="Categorie non trouvee")
        return categorie
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/prix-moyen/", response_model=List[PrixMoyenCategorie])
def obtenir_prix_moyen_par_categorie():
    """
    Calculer et retourner le prix moyen des livres par catégorie.

    Returns:
        List[PrixMoyenCategorie]: Liste des catégories avec leur prix moyen,
                                  nombre de livres, triée par prix décroissant
    """
    try:
        return book_service.calculer_prix_moyen_par_categorie()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/top-nombre-livres/", response_model=List[TopCategorie])
def obtenir_top_categories_par_nombre_livres():
    """
    Obtenir le classement des catégories par nombre de livres.

    Returns:
        List[TopCategorie]: Liste des catégories classées par nombre de livres décroissant,
                           avec rang, nombre de livres et pourcentage du total
    """
    try:
        return book_service.obtenir_top_categories_par_nombre_livres()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")