from typing import List, Optional
from api.interfaces.book_service_interface import BookServiceInterface
from api.repositories.book_repository_sql import BookRepositorySQL
from api.models.book import Book
from api.models.prix_moyen_categorie import PrixMoyenCategorie
from api.models.top_categorie import TopCategorie


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

    def calculer_prix_moyen_par_categorie(self) -> List[PrixMoyenCategorie]:
        """
        Calculer le prix moyen des livres par catégorie.

        Returns:
            List[PrixMoyenCategorie]: Liste des prix moyens par catégorie
        """
        tous_les_livres = self.book_repository.get_all_books()

        # Dictionnaire pour regrouper par catégorie
        categories_dict = {}

        for livre in tous_les_livres:
            if livre.categorie and livre.prix_numerique > 0:
                if livre.categorie not in categories_dict:
                    categories_dict[livre.categorie] = {
                        'total_prix': 0.0,
                        'nombre_livres': 0
                    }

                categories_dict[livre.categorie]['total_prix'] += livre.prix_numerique
                categories_dict[livre.categorie]['nombre_livres'] += 1

        # Calculer les prix moyens
        resultats = []
        for categorie, data in categories_dict.items():
            if data['nombre_livres'] > 0:
                prix_moyen = round(data['total_prix'] / data['nombre_livres'], 2)
                resultats.append(PrixMoyenCategorie(
                    categorie=categorie,
                    prix_moyen=prix_moyen,
                    nombre_livres=data['nombre_livres']
                ))

        # Trier par prix moyen décroissant
        resultats.sort(key=lambda x: x.prix_moyen, reverse=True)
        return resultats

    def obtenir_top_categories_par_nombre_livres(self) -> List[TopCategorie]:
        """
        Obtenir le classement des catégories par nombre de livres.

        Returns:
            List[TopCategorie]: Liste des catégories classées par nombre de livres décroissant
        """
        tous_les_livres = self.book_repository.get_all_books()

        # Dictionnaire pour compter les livres par catégorie
        categories_count = {}

        for livre in tous_les_livres:
            if livre.categorie:
                if livre.categorie not in categories_count:
                    categories_count[livre.categorie] = 0
                categories_count[livre.categorie] += 1

        # Trier par nombre de livres décroissant
        categories_triees = sorted(categories_count.items(), key=lambda x: x[1], reverse=True)

        # Calculer le total pour les pourcentages
        total_livres = sum(categories_count.values())

        # Créer le classement avec rang
        resultats = []
        for rang, (categorie, nombre_livres) in enumerate(categories_triees, 1):
            pourcentage = round((nombre_livres / total_livres) * 100, 2) if total_livres > 0 else 0.0

            resultats.append(TopCategorie(
                rang=rang,
                categorie=categorie,
                nombre_livres=nombre_livres,
                pourcentage_total=pourcentage
            ))

        return resultats
