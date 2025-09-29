import json
import os
from typing import List, Optional
from api.interfaces.book_repository_interface import BookRepositoryInterface
from api.models.book import Book


class BookRepository(BookRepositoryInterface):
    """
    Classe de dépôt pour gérer les livres depuis les fichiers JSON générés par Scrapy.
    """

    def __init__(self):
        """
        Initialiser le repository avec les chemins vers les fichiers JSON.
        """
        self.base_path = "books_toscrape"
        self.books: List[Book] = []
        self.charger_donnees_livres()

    def charger_donnees_livres(self) -> None:
        """
        Charger les données des livres depuis les fichiers JSON de Scrapy.
        """
        try:
            # Charger d'abord detail_books.json (données les plus complètes)
            detail_books_path = os.path.join(self.base_path, "detail_books.json")
            if os.path.exists(detail_books_path):
                with open(detail_books_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    self.books = [self.convertir_json_vers_book(item, index + 1)
                                 for index, item in enumerate(json_data)]
                    return

            # Si pas de détails, charger books_by_categories.json
            books_categories_path = os.path.join(self.base_path, "books_by_categories.json")
            if os.path.exists(books_categories_path):
                with open(books_categories_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    self.books = [self.convertir_json_vers_book(item, index + 1)
                                 for index, item in enumerate(json_data)]

        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            self.books = []

    def convertir_json_vers_book(self, json_data: dict, book_id: int) -> Book:
        """
        Convertir les données JSON en objet Book.

        Args:
            json_data: Les données JSON du livre
            book_id: L'ID à assigner au livre

        Returns:
            Book: L'objet Book créé
        """
        return Book(
            id=json_data.get('id', book_id),
            url_page=json_data.get('url_page', json_data.get('url', '')),
            categorie=json_data.get('categorie', json_data.get('category', '')),
            title=json_data.get('titre', json_data.get('title', '')),
            prix_numerique=float(json_data.get('prix_numerique', 0.0)),
            note_etoiles_nombre=int(json_data.get('note_etoiles', 0)),
            nombre_avis_clients=int(json_data.get('nombre_avis', 0)),
            en_stock=json_data.get('disponibilite', '').lower().startswith('in stock'),
            nombre_stock=int(json_data.get('nombre_stock', 0)),
            description=json_data.get('description', ''),
            url_image=json_data.get('url_image', json_data.get('image_url', '')),
            nom_fichier_image='',
            alt_image='',
            fil_ariane=str(json_data.get('fil_ariane', [])),
            code_upc=json_data.get('code_upc', ''),
            type_produit=json_data.get('type_produit', 'Books'),
            taxe=float(json_data.get('taxe', 0.0)),
            nombre_avis=int(json_data.get('nombre_avis', 0))
        )

    def get_all_books(self) -> List[Book]:
        """
        Récupérer tous les livres stockés.

        Returns:
            List[Book]: Liste de tous les livres
        """
        return self.books

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Récupérer un livre par son ID.

        Args:
            book_id: L'ID du livre à récupérer

        Returns:
            Optional[Book]: Le livre trouvé ou None
        """
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def save_book(self, book: Book) -> Book:
        """
        Sauvegarder un nouveau livre.

        Args:
            book: Le livre à sauvegarder

        Returns:
            Book: Le livre sauvegardé avec son ID
        """
        # Générer un nouvel ID
        max_id = max([b.id for b in self.books if b.id], default=0)
        book.id = max_id + 1

        # Ajouter à la liste
        self.books.append(book)

        return book

    def update_book(self, book_id: int, book_data: Book) -> Optional[Book]:
        """
        Mettre à jour un livre existant.

        Args:
            book_id: L'ID du livre à mettre à jour
            book_data: Les nouvelles données du livre

        Returns:
            Optional[Book]: Le livre mis à jour ou None si non trouvé
        """
        for index, book in enumerate(self.books):
            if book.id == book_id:
                # Conserver l'ID original
                book_data.id = book_id
                self.books[index] = book_data
                return book_data
        return None

    def delete_book(self, book_id: int) -> bool:
        """
        Supprimer un livre par son ID.

        Args:
            book_id: L'ID du livre à supprimer

        Returns:
            bool: True si supprimé, False sinon
        """
        for index, book in enumerate(self.books):
            if book.id == book_id:
                del self.books[index]
                return True
        return False

    def find_by_category(self, category: str) -> List[Book]:
        """
        Rechercher des livres par catégorie.

        Args:
            category: Le nom de la catégorie à rechercher

        Returns:
            List[Book]: Liste des livres de cette catégorie
        """
        return [
            book for book in self.books
            if book.categorie.lower() == category.lower()
        ]

