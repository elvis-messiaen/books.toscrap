# -*- coding: utf-8 -*-
from typing import List
from fastapi import APIRouter, HTTPException
from api.services.category_service import CategoryService

router = APIRouter()
category_service = CategoryService()


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