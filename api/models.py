"""
Mod�les Pydantic pour la validation et s�rialisation des donn�es de l'API.

Ce module contient tous les sch�mas de donn�es utilis�s par l'API FastAPI
pour valider les requ�tes entrantes et formater les r�ponses sortantes.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, validator


class CategorieModel(BaseModel):
    """
    Mod�le repr�sentant une cat�gorie de livres.

    Attributes:
        nom: Nom de la cat�gorie
        url: URL compl�te de la cat�gorie
        url_relative: URL relative de la cat�gorie
    """
    nom: str = Field(..., description="Nom de la cat�gorie")
    url: str = Field(..., description="URL compl�te de la cat�gorie")
    url_relative: str = Field(..., description="URL relative de la cat�gorie")

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
    Mod�le simplifi� d'un livre pour les listes.

    Attributes:
        titre: Titre du livre
        prix: Prix du livre
        note_etoiles: Note en �toiles (One, Two, Three, Four, Five)
        url_image: URL de l'image de couverture
        url: URL de la page d�taill�e du livre
        categorie: Cat�gorie du livre (optionnel)
        disponibilite: Information de disponibilit� (optionnel)
    """
    titre: str = Field(..., description="Titre du livre")
    prix: str = Field(..., description="Prix du livre")
    note_etoiles: str = Field(..., description="Note en �toiles")
    url_image: str = Field(..., description="URL de l'image de couverture")
    url: str = Field(..., description="URL de la page d�taill�e")
    categorie: Optional[str] = Field(None, description="Cat�gorie du livre")
    disponibilite: Optional[str] = Field(None, description="Information de disponibilit�")

    @validator('note_etoiles')
    def valider_note_etoiles(cls, v):
        """
        Valider que la note en �toiles est dans les valeurs autoris�es.

        Args:
            v: Valeur � valider

        Returns:
            str: Valeur valid�e

        Raises:
            ValueError: Si la valeur n'est pas valide
        """
        notes_valides = ['One', 'Two', 'Three', 'Four', 'Five']
        if v not in notes_valides:
            raise ValueError(f'Note doit �tre une de: {notes_valides}')
        return v

    class Config:
        schema_extra = {
            "example": {
                "titre": "Sharp Objects",
                "prix": "�47.82",
                "note_etoiles": "Four",
                "url_image": "https://books.toscrape.com/media/cache/32/51/...",
                "url": "https://books.toscrape.com/catalogue/sharp-objects_997/index.html",
                "categorie": "Mystery",
                "disponibilite": "In stock (20 available)"
            }
        }