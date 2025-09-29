from typing import List, Optional
from api.interfaces.categories_service_interface import CategoryServiceInterface
from api.repositories.category_repository import CategoryRepository


class CategoryService(CategoryServiceInterface):
    """
    Service pour gérer la logique métier des catégories.
    Fait le lien entre les contrôleurs et le repository.
    """

    def __init__(self):
        """
        Initialiser le service avec une instance de CategoryRepository.
        """
        self.category_repository = CategoryRepository()

    def get_all_categories(self) -> List[dict]:
        """
        Récupérer toutes les catégories.

        Returns:
            List[dict]: Liste de toutes les catégories
        """
        return self.category_repository.get_all_categories()

    def get_category_by_id(self, category_id: int) -> Optional[dict]:
        """
        Récupérer une catégorie par son ID avec validation.

        Args:
            category_id: L'ID de la catégorie à récupérer

        Returns:
            dict: La catégorie trouvée ou None

        Raises:
            ValueError: Si l'ID est invalide
        """
        if category_id <= 0:
            raise ValueError("L'ID de la catégorie doit être un nombre positif")

        return self.category_repository.get_category_by_id(category_id)

    def create_category(self, category_data: dict) -> dict:
        """
        Créer une nouvelle catégorie avec validation métier.

        Args:
            category_data: Les données de la catégorie à créer

        Returns:
            dict: La catégorie créée

        Raises:
            ValueError: Si les données sont invalides
        """
        # Validation métier simple
        if not category_data.get('nom'):
            raise ValueError("Le nom de la catégorie est obligatoire")

        return self.category_repository.save_category(category_data)

    def update_category(self, category_id: int, category_data: dict) -> Optional[dict]:
        """
        Mettre à jour une catégorie existante.

        Args:
            category_id: L'ID de la catégorie à mettre à jour
            category_data: Les nouvelles données de la catégorie

        Returns:
            dict: La catégorie mise à jour ou None
        """
        if category_id <= 0:
            raise ValueError("L'ID de la catégorie doit être un nombre positif")

        if not category_data.get('nom'):
            raise ValueError("Le nom de la catégorie est obligatoire")

        return self.category_repository.update_category(category_id, category_data)

    def delete_category(self, category_id: int) -> bool:
        """
        Supprimer une catégorie par son ID.

        Args:
            category_id: L'ID de la catégorie à supprimer

        Returns:
            bool: True si supprimée, False sinon
        """
        if category_id <= 0:
            raise ValueError("L'ID de la catégorie doit être un nombre positif")

        return self.category_repository.delete_category(category_id)
