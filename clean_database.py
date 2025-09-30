#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vider la base de données avant un nouveau scraping
"""

from database_config import engine
from sqlalchemy import text

def vider_base_donnees():
    """
    Vide complètement la table books pour un scraping propre
    """
    try:
        with engine.connect() as connection:
            # Supprimer tous les enregistrements de la table books
            result = connection.execute(text("DELETE FROM books"))
            connection.commit()

            print(f"Table books vidée - {result.rowcount} enregistrements supprimés")

            # Remettre l'auto-increment à 1
            connection.execute(text("ALTER SEQUENCE books_id_seq RESTART WITH 1"))
            connection.commit()

            print("Séquence ID remise à 1")
            print("Base de données prête pour un nouveau scraping!")

    except Exception as e:
        print(f"Erreur lors du vidage: {e}")
        raise e

def tester_connexion():
    """
    Teste la connexion à la base de données
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM books"))
            count = result.scalar()
            print(f"Nombre d'enregistrements actuels: {count}")
            return True
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        return False

if __name__ == "__main__":
    print("Préparation de la base de données...")

    if tester_connexion():
        vider_base_donnees()
    else:
        print("Impossible de se connecter à la base de données")
        exit(1)