from abc import ABC, abstractmethod


class CategoryServiceInterface(ABC):

    """
    récupérer toutes les catégories
    """
    @abstractmethod
    def get_all_categories(self) -> list[dict]:
        pass

    """
    récupérer une catégorie par son ID
    """
    @abstractmethod
    def get_category_by_id(self, category_id: int) -> dict:
        pass

    """
    créer une nouvelle catégorie avec validation métier
    """
    @abstractmethod
    def create_category(self, category_data: dict) -> dict:
        pass

    """
    mettre à jour une catégorie existante
    """
    @abstractmethod
    def update_category(self, category_id: int, category_data: dict) -> dict:
        pass

    """
    supprimer une catégorie par son ID
    """
    @abstractmethod
    def delete_category(self, category_id: int) -> bool:
        pass

