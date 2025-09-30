# -*- coding: utf-8 -*-
"""
Repository PostgreSQL pour gerer les livres.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from api.interfaces.book_repository_interface import BookRepositoryInterface
from api.models.book import Book
from api.models.book_sql import BookSQL
from database_config import SessionLocal


class BookRepositorySQL(BookRepositoryInterface):
    """
    Repository PostgreSQL pour gerer les livres.
    """

    def __init__(self):
        """
        Initialiser le repository PostgreSQL.
        """
        pass

    def obtenir_session_db(self) -> Session:
        """
        Obtenir une session de base de donnees.

        Returns:
            Session: Session SQLAlchemy
        """
        return SessionLocal()

    def convertir_sql_vers_book(self, book_sql: BookSQL) -> Book:
        """
        Convertir un objet SQLAlchemy en dataclass Book.

        Args:
            book_sql: Objet BookSQL

        Returns:
            Book: Objet Book dataclass
        """
        return Book(
            id=book_sql.id,
            url_page=book_sql.url_page or "",
            categorie=book_sql.categorie or "",
            title=book_sql.title or "",
            prix_numerique=book_sql.prix_numerique or 0.0,
            note_etoiles_nombre=book_sql.note_etoiles_nombre or 0,
            nombre_avis_clients=book_sql.nombre_avis_clients or 0,
            en_stock=book_sql.en_stock or False,
            nombre_stock=book_sql.nombre_stock or 0,
            description=book_sql.description or "",
            url_image=book_sql.url_image or "",
            nom_fichier_image=book_sql.nom_fichier_image or "",
            alt_image=book_sql.alt_image or "",
            fil_ariane=book_sql.fil_ariane or "",
            code_upc=book_sql.code_upc or "",
            type_produit=book_sql.type_produit or "Books",
            taxe=book_sql.taxe or 0.0,
            nombre_avis=book_sql.nombre_avis or 0
        )

    def convertir_book_vers_sql(self, book: Book) -> BookSQL:
        """
        Convertir un objet Book en BookSQL.

        Args:
            book: Objet Book dataclass

        Returns:
            BookSQL: Objet SQLAlchemy
        """
        book_sql = BookSQL()
        book_sql.from_dataclass(book)
        return book_sql

    def get_all_books(self) -> List[Book]:
        """
        Recuperer tous les livres depuis PostgreSQL.

        Returns:
            List[Book]: Liste de tous les livres
        """
        db = self.obtenir_session_db()
        try:
            books_sql = db.query(BookSQL).all()
            return [self.convertir_sql_vers_book(book_sql) for book_sql in books_sql]
        finally:
            db.close()

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Recuperer un livre par son ID depuis PostgreSQL.

        Args:
            book_id: L'ID du livre a recuperer

        Returns:
            Optional[Book]: Le livre trouve ou None
        """
        db = self.obtenir_session_db()
        try:
            book_sql = db.query(BookSQL).filter(BookSQL.id == book_id).first()
            if book_sql:
                return self.convertir_sql_vers_book(book_sql)
            return None
        finally:
            db.close()

    def save_book(self, book: Book) -> Book:
        """
        Sauvegarder un nouveau livre dans PostgreSQL.

        Args:
            book: Le livre a sauvegarder

        Returns:
            Book: Le livre sauvegarde avec son ID
        """
        db = self.obtenir_session_db()
        try:
            book_sql = self.convertir_book_vers_sql(book)
            db.add(book_sql)
            db.commit()
            db.refresh(book_sql)
            return self.convertir_sql_vers_book(book_sql)
        finally:
            db.close()

    def find_by_category(self, category: str) -> List[Book]:
        """
        Rechercher des livres par categorie dans PostgreSQL.

        Args:
            category: Le nom de la categorie a rechercher

        Returns:
            List[Book]: Liste des livres de cette categorie
        """
        db = self.obtenir_session_db()
        try:
            books_sql = db.query(BookSQL).filter(
                BookSQL.categorie.ilike(f"%{category}%")
            ).all()
            return [self.convertir_sql_vers_book(book_sql) for book_sql in books_sql]
        finally:
            db.close()