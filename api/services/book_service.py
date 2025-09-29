from typing import List, Optional
from api.interfaces.book_service_interface import BookServiceInterface
from api.repositories.book_repository import BookRepository
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
        self.book_repository = BookRepository()

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

    def create_book(self, book_data: Book) -> Book:
        """
        Créer un nouveau livre avec validation métier.

        Args:
            book_data: Les données du livre à créer

        Returns:
            Book: Le livre créé

        Raises:
            ValueError: Si les données sont invalides
        """
        # Validation métier
        self.valider_livre(book_data)

        # Sauvegarder via le repository
        return self.book_repository.save_book(book_data)

    def update_book(self, book_id: int, book_data: Book) -> Optional[Book]:
        """
        Mettre à jour un livre existant avec validation.

        Args:
            book_id: L'ID du livre à mettre à jour
            book_data: Les nouvelles données du livre

        Returns:
            Optional[Book]: Le livre mis à jour ou None

        Raises:
            ValueError: Si les données sont invalides
        """
        if book_id <= 0:
            raise ValueError("L'ID du livre doit être un nombre positif")

        # Vérifier que le livre existe
        if not self.book_repository.get_book_by_id(book_id):
            return None

        # Validation métier
        self.valider_livre(book_data)

        return self.book_repository.update_book(book_id, book_data)

    def delete_book(self, book_id: int) -> bool:
        """
        Supprimer un livre par son ID avec vérifications.

        Args:
            book_id: L'ID du livre à supprimer

        Returns:
            bool: True si supprimé, False sinon

        Raises:
            ValueError: Si l'ID est invalide
        """
        if book_id <= 0:
            raise ValueError("L'ID du livre doit être un nombre positif")

        return self.book_repository.delete_book(book_id)

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

    def valider_livre(self, book: Book) -> None:
        """
        Valider les données d'un livre selon les règles métier.

        Args:
            book: Le livre à valider

        Raises:
            ValueError: Si les données sont invalides
        """
        # Validation du titre
        if not book.title or not book.title.strip():
            raise ValueError("Le titre est obligatoire")

        # Validation du prix
        if book.prix_numerique < 0:
            raise ValueError("Le prix ne peut pas être négatif")

        # Validation de la note
        if book.note_etoiles_nombre and not 1 <= book.note_etoiles_nombre <= 5:
            raise ValueError("La note doit être entre 1 et 5")