from abc import ABC, abstractmethod
from typing import List, Optional
from api.models.book import Book


class BookRepositoryInterface(ABC):
    """
    Interface definissant les operations de lecture seule pour les livres.
    """

    @abstractmethod
    def get_all_books(self) -> List[Book]:
        """
        Recuperer tous les livres.

        Returns:
            List[Book]: Liste de tous les livres
        """
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Recuperer un livre par son ID.

        Args:
            book_id: L'ID du livre a recuperer

        Returns:
            Optional[Book]: Le livre trouve ou None
        """
        pass

    @abstractmethod
    def save_book(self, book: Book) -> Book:
        """
        Sauvegarder un nouveau livre.

        Args:
            book: Le livre a sauvegarder

        Returns:
            Book: Le livre sauvegarde avec son ID
        """
        pass

    @abstractmethod
    def find_by_category(self, category: str) -> List[Book]:
        """
        Rechercher des livres par categorie.

        Args:
            category: Le nom de la categorie a rechercher

        Returns:
            List[Book]: Liste des livres de cette categorie
        """
        pass
