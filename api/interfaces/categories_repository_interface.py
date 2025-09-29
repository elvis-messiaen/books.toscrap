from abc import ABC, abstractmethod


class CategoryRepositoryInterface(ABC):

    """
    Recupérer toutes les catégories
    """
    @abstractmethod
    def get_all_categories(self) -> list[dict]:
        pass

    """
    Recupérer une catégorie par son ID
    """
    @abstractmethod
    def get_category_by_id(self, category_id: int) -> dict:
        pass

    """
    Sauvegarder une nouvelle catégorie
    """
    @abstractmethod
    def save_category(self, category: dict) -> dict:
        pass

    """
    Mettre à jour une catégorie existante
    """
    @abstractmethod
    def update_category(self, category_id: int, category: dict) -> dict:
        pass

    """
    Supprimer une catégorie par son ID
    """
    @abstractmethod
    def delete_category(self, category_id: int) -> bool:
        pass
