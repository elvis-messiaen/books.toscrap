# -*- coding: utf-8 -*-
"""
Modèle pour le prix moyen par catégorie.
"""
from dataclasses import dataclass


@dataclass
class PrixMoyenCategorie:
    """
    Modèle représentant le prix moyen d'une catégorie.
    """
    categorie: str
    prix_moyen: float
    nombre_livres: int