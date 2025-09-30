# -*- coding: utf-8 -*-
"""
Modele SQLAlchemy pour les livres.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from database_config import Base


class BookSQL(Base):
    """
    Modele SQLAlchemy pour les livres.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url_page = Column(String(500), nullable=True)
    categorie = Column(String(100), nullable=True, index=True)
    title = Column(String(500), nullable=True, index=True)
    titre_complet = Column(String(500), nullable=True)
    prix_numerique = Column(Float, nullable=True, default=0.0)
    note_etoiles_nombre = Column(Integer, nullable=True, default=0)
    nombre_avis_clients = Column(Integer, nullable=True, default=0)
    en_stock = Column(Boolean, nullable=True, default=False)
    nombre_stock = Column(Integer, nullable=True, default=0)
    description = Column(Text, nullable=True)
    url_image = Column(String(500), nullable=True)
    nom_fichier_image = Column(String(200), nullable=True)
    alt_image = Column(String(200), nullable=True)
    fil_ariane = Column(Text, nullable=True)
    code_upc = Column(String(50), nullable=True)
    type_produit = Column(String(50), nullable=True, default="Books")
    taxe = Column(Float, nullable=True, default=0.0)
    nombre_avis = Column(Integer, nullable=True, default=0)

    def to_dict(self):
        """
        Convertir l'objet SQLAlchemy en dictionnaire.

        Returns:
            dict: Representation dictionnaire de l'objet
        """
        return {
            "id": self.id,
            "url_page": self.url_page,
            "categorie": self.categorie,
            "title": self.title,
            "titre_complet": self.titre_complet,
            "prix_numerique": self.prix_numerique,
            "note_etoiles_nombre": self.note_etoiles_nombre,
            "nombre_avis_clients": self.nombre_avis_clients,
            "en_stock": self.en_stock,
            "nombre_stock": self.nombre_stock,
            "description": self.description,
            "url_image": self.url_image,
            "nom_fichier_image": self.nom_fichier_image,
            "alt_image": self.alt_image,
            "fil_ariane": self.fil_ariane,
            "code_upc": self.code_upc,
            "type_produit": self.type_produit,
            "taxe": self.taxe,
            "nombre_avis": self.nombre_avis
        }

    def from_dataclass(self, book_dataclass):
        """
        Remplir l'objet SQLAlchemy depuis une dataclass Book.

        Args:
            book_dataclass: Instance de la dataclass Book
        """
        self.url_page = book_dataclass.url_page
        self.categorie = book_dataclass.categorie
        self.title = book_dataclass.title
        self.prix_numerique = book_dataclass.prix_numerique
        self.note_etoiles_nombre = book_dataclass.note_etoiles_nombre
        self.nombre_avis_clients = book_dataclass.nombre_avis_clients
        self.en_stock = book_dataclass.en_stock
        self.nombre_stock = book_dataclass.nombre_stock
        self.description = book_dataclass.description
        self.url_image = book_dataclass.url_image
        self.nom_fichier_image = book_dataclass.nom_fichier_image
        self.alt_image = book_dataclass.alt_image
        self.fil_ariane = book_dataclass.fil_ariane
        self.code_upc = book_dataclass.code_upc
        self.type_produit = book_dataclass.type_produit
        self.taxe = book_dataclass.taxe
        self.nombre_avis = book_dataclass.nombre_avis

    def __repr__(self):
        return f"<BookSQL(id={self.id}, title='{self.title}', categorie='{self.categorie}')>"