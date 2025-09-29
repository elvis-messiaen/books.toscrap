from abc import ABC, abstractmethod
from typing import List, Optional
from api.models.book import Book


class BookRepositoryInterface(ABC):
    """
    Interface définissant les opérations de persistance pour les livres.
    """

    @abstractmethod
    def get_all_books(self) -> List[Book]:
        """
        Récupérer tous les livres.

        Returns:
            List[Book]: Liste de tous les livres
        """
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Récupérer un livre par son ID.

        Args:
            book_id: L'ID du livre à récupérer

        Returns:
            Optional[Book]: Le livre trouvé ou None
        """
        pass

    @abstractmethod
    def save_book(self, book: Book) -> Book:
        """
        Sauvegarder un nouveau livre.

        Args:
            book: Le livre à sauvegarder

        Returns:
            Book: Le livre sauvegardé avec son ID
        """
        pass

    @abstractmethod
    def update_book(self, book_id: int, book: Book) -> Optional[Book]:
        """
        Mettre à jour un livre existant.

        Args:
            book_id: L'ID du livre à mettre à jour
            book: Les nouvelles données du livre

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
