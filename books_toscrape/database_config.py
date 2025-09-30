# -*- coding: utf-8 -*-
"""
Configuration de la base de donnees PostgreSQL.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Parametres de connexion PostgreSQL
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "books_scraping",
    "user": "elvis",
    "password": "azerty@&123"
}

# URL de connexion SQLAlchemy avec encodage des caracteres speciaux
from urllib.parse import quote_plus

DATABASE_URL = f"postgresql://{DATABASE_CONFIG['user']}:{quote_plus(DATABASE_CONFIG['password'])}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

# Configuration SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_database_session():
    """
    Obtenir une session de base de donnees.

    Returns:
        Session: Session SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Creer toutes les tables dans la base de donnees.
    """
    Base.metadata.create_all(bind=engine)


def test_connection():
    """
    Tester la connexion a la base de donnees.

    Returns:
        bool: True si la connexion fonctionne
    """
    try:
        with engine.connect() as connection:
            print("Connexion a PostgreSQL reussie !")
            return True
    except Exception as e:
        print(f"Erreur de connexion PostgreSQL: {e}")
        return False