"""
Modèles Pydantic pour la validation et sérialisation des données de l'API.

Ce module contient tous les schémas de données utilisés par l'API FastAPI
pour valider les requêtes entrantes et formater les réponses sortantes.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, validator


class CategorieModel(BaseModel):
    """
    Modèle représentant une catégorie de livres.

    Attributes:
        nom: Nom de la catégorie
        url: URL complète de la catégorie
        url_relative: URL relative de la catégorie
    """
    nom: str = Field(..., description="Nom de la catégorie")
    url: str = Field(..., description="URL complète de la catégorie")
    url_relative: str = Field(..., description="URL relative de la catégorie")

    class Config:
        schema_extra = {
            "example": {
                "nom": "Mystery",
                "url": "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
                "url_relative": "catalogue/category/books/mystery_3/index.html"
            }
        }


class LivreSimpleModel(BaseModel):
    """
    Modèle simplifié d'un livre pour les listes.

    Attributes:
        titre: Titre du livre
        prix: Prix du livre
        note_etoiles: Note en étoiles (One, Two, Three, Four, Five)
        url_image: URL de l'image de couverture
        url: URL de la page détaillée du livre
        categorie: Catégorie du livre (optionnel)
        disponibilite: Information de disponibilité (optionnel)
    """
    titre: str = Field(..., description="Titre du livre")
    prix: str = Field(..., description="Prix du livre")
    note_etoiles: str = Field(..., description="Note en étoiles")
    url_image: str = Field(..., description="URL de l'image de couverture")
    url: str = Field(..., description="URL de la page détaillée")
    categorie: Optional[str] = Field(None, description="Catégorie du livre")
    disponibilite: Optional[str] = Field(None, description="Information de disponibilité")

    @validator('note_etoiles')
    def valider_note_etoiles(cls, v):
        """
        Valider que la note en étoiles est dans les valeurs autorisées.

        Args:
            v: Valeur à valider

        Returns:
            str: Valeur validée

        Raises:
            ValueError: Si la valeur n'est pas valide
        """
        notes_valides = ['One', 'Two', 'Three', 'Four', 'Five']
        if v not in notes_valides:
            raise ValueError(f'Note doit être une de: {notes_valides}')
        return v

    class Config:
        schema_extra = {
            "example": {
                "titre": "Sharp Objects",
                "prix": "£47.82",
                "note_etoiles": "Four",
                "url_image": "https://books.toscrape.com/media/cache/32/51/...",
                "url": "https://books.toscrape.com/catalogue/sharp-objects_997/index.html",
                "categorie": "Mystery",
                "disponibilite": "In stock (20 available)"
            }
        }