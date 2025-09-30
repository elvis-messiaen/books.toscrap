from typing import List, Optional
from api.interfaces.book_service_interface import BookServiceInterface
from api.repositories.book_repository_sql import BookRepositorySQL
from api.models.book import Book


class BookService(BookServiceInterface):
    """
    Service pour gérer la logique métier des livres.
    Fait le lien entre les contrôleurs et le repository.
    """

    def __init__(self):
        """
        Initialiser le service avec une instance de BookRepository.
        """
        self.book_repository = BookRepositorySQL()

    def get_all_books(self) -> List[Book]:
        """
        Récupérer tous les livres avec validation métier.

        Returns:
            List[Book]: Liste de tous les livres
        """
        return self.book_repository.get_all_books()

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Récupérer un livre par son ID avec validation.

        Args:
            book_id: L'ID du livre à récupérer

        Returns:
            Optional[Book]: Le livre trouvé ou None

        Raises:
            ValueError: Si l'ID est invalide
        """
        if book_id <= 0:
            raise ValueError("L'ID du livre doit être un nombre positif")

        return self.book_repository.get_book_by_id(book_id)




    def find_by_category(self, category: str) -> List[Book]:
        """
        Rechercher des livres par catégorie avec normalisation.

        Args:
            category: Le nom de la catégorie à rechercher

        Returns:
            List[Book]: Liste des livres de cette catégorie

        Raises:
            ValueError: Si la catégorie est vide
        """
        if not category or not category.strip():
            raise ValueError("Le nom de la catégorie ne peut pas être vide")

        # Normaliser le nom de la catégorie
        category = category.strip()

        return self.book_repository.find_by_category(category)
