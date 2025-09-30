# -*- coding: utf-8 -*-
import json
import os
from typing import List, Optional
from api.interfaces.categories_repository_interface import CategoryRepositoryInterface


class CategoryRepository(CategoryRepositoryInterface):
    """Classe de depot pour gerer les categories depuis les fichiers JSON generes par Scrapy."""

    def __init__(self):
        """Initialiser le repository avec les chemins vers les fichiers JSON."""
        self.base_path = "books_toscrape"
        self.categories_data = []
        self.charger_donnees_categories()

    def charger_donnees_categories(self) -> None:
        """Charger les donnees des categories depuis le fichier JSON de Scrapy."""
        try:
            categories_path = os.path.join(self.base_path, "categories.json")
            if os.path.exists(categories_path):
                with open(categories_path, 'r', encoding='utf-8') as f:
                    self.categories_data = json.load(f)
                    self.ajouter_ids_aux_categories()
        except Exception as e:
            print(f"Erreur lors du chargement des categories: {e}")
            self.categories_data = []

    def ajouter_ids_aux_categories(self) -> None:
        """Ajouter des IDs uniques aux categories s'ils n'en ont pas."""
        for index, category in enumerate(self.categories_data):
            if 'id' not in category:
                category['id'] = index + 1

    def get_all_categories(self) -> List[dict]:
        """Recuperer toutes les categories stockees."""
        return self.categories_data

    def get_category_by_id(self, category_id: int) -> Optional[dict]:
        """Recuperer une categorie par son ID."""
        for category in self.categories_data:
            if category.get('id') == category_id:
                return category
        return None

    def save_category(self, category: dict) -> dict:
        """Sauvegarder une nouvelle categorie."""
        max_id = max([c.get('id', 0) for c in self.categories_data], default=0)
        category['id'] = max_id + 1
        self.categories_data.append(category)
        return category


