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

