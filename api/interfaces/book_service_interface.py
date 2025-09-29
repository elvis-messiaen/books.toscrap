from abc import ABC, abstractmethod
from typing import List, Optional
from api.models.book import Book


class BookServiceInterface(ABC):
    """
    Interface définissant les opérations métier pour les livres.
    """

    @abstractmethod
    def get_all_books(self) -> List[Book]:
        """
        Récupérer tous les livres avec validation métier.

        Returns:
            List[Book]: Liste de tous les livres
        """
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Récupérer un livre par son ID avec validation.

        Args:
            book_id: L'ID du livre à récupérer

        Returns:
            Optional[Book]: Le livre trouvé ou None
        """
        pass

    @abstractmethod
    def create_book(self, book_data: Book) -> Book:
        """
        Créer un nouveau livre avec validation métier.

        Args:
            book_data: Les données du livre à créer

        Returns:
            Book: Le livre créé
        """
        pass

    @abstractmethod
    def update_book(self, book_id: int, book_data: Book) -> Optional[Book]:
        """
        Mettre à jour un livre existant avec validation.

        Args:
            book_id: L'ID du livre à mettre à jour
            book_data: Les nouvelles données du livre

        Returns:
            Optional[Book]: Le livre mis à jour ou None
        """
        pass

    @abstractmethod
    def delete_book(self, book_id: int) -> bool:
        """
        Supprimer un livre par son ID.

        Args:
            book_id: L'ID du livre à supprimer

        Returns:
            bool: True si supprimé, False sinon
        """
        pass

    @abstractmethod
    def find_by_category(self, category: str) -> List[Book]:
        """
        Rechercher des livres par catégorie.

        Args:
            category: Le nom de la catégorie à rechercher

        Returns:
            List[Book]: Liste des livres de cette catégorie
        """
        pass
