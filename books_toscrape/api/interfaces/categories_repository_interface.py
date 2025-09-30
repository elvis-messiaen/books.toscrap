from abc import ABC, abstractmethod


class CategoryRepositoryInterface(ABC):
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

    @abstractmethod
    def save_category(self, category: dict) -> dict:
        """
        Sauvegarder une nouvelle categorie.

        Args:
            category: La categorie a sauvegarder

        Returns:
            dict: La categorie sauvegardee avec son ID
        """
        pass
