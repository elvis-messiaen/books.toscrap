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


@router.post("/")
def creer_categorie(categorie: dict):
    """Creer une nouvelle categorie."""
    try:
        return category_service.create_category(categorie)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.put("/{category_id}")
def modifier_categorie(category_id: int, categorie: dict):
    """Mettre a jour une categorie existante."""
    try:
        categorie_modifiee = category_service.update_category(category_id, categorie)
        if not categorie_modifiee:
            raise HTTPException(status_code=404, detail="Categorie non trouvee")
        return categorie_modifiee
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.delete("/{category_id}")
def supprimer_categorie(category_id: int):
    """Supprimer une categorie par son ID."""
    try:
        supprime = category_service.delete_category(category_id)
        if not supprime:
            raise HTTPException(status_code=404, detail="Categorie non trouvee")
        return {"message": f"Categorie {category_id} supprimee avec succes"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")