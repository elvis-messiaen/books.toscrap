# -*- coding: utf-8 -*-
"""
Modèle pour le top des catégories par nombre de livres.
"""
from dataclasses import dataclass


@dataclass
class TopCategorie:
    """
    Modèle représentant une catégorie dans le classement par nombre de livres.
    """
    rang: int
    categorie: str
    nombre_livres: int
    pourcentage_total: float