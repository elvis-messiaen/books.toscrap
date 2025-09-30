from abc import ABC, abstractmethod


class CategoryServiceInterface(ABC):
    """
    Interface definissant les operations de lecture seule pour les categories.
    """

    @abstractmethod
    def get_all_categories(self) -> list[dict]:
        """
        Recuperer toutes les categories.

        Returns:
            list[dict]: Liste de toutes les categories
        """
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> dict:
        """
        Recuperer une categorie par son ID.

        Args:
            category_id: L'ID de la categorie a recuperer

        Returns:
            dict: La categorie trouvee ou None
        """
        pass

