"""
Spider pour extraire tous les livres organisés par catégorie

Ce spider lit le fichier JSON des catégories généré par categories_spider,
puis pour chaque catégorie, extrait tous les livres qu'elle contient.
Chaque livre est associé à sa catégorie d'origine.

PRÉREQUIS: Exécuter d'abord "scrapy crawl categories_spider -o categories.json"
"""
import scrapy
import json
import os


class BooksByCategoriesSpider(scrapy.Spider):
    """
    Spider pour scraper tous les livres triés par catégorie

    Ce spider optimisé lit le fichier categories.json existant
    au lieu de re-scrapper les catégories, puis visite chaque page
    de catégorie pour extraire tous les livres.
    """
    name = "books_by_categories"
    allowed_domains = ["books.toscrape.com"]

    def start_requests(self):
        """
        Méthode d'entrée qui lit le fichier JSON des catégories

        Lit le fichier categories.json et génère une requête
        pour chaque catégorie trouvée.

        Yields:
            Request: Requêtes vers chaque page de catégorie
        """
        # Chemin vers le fichier JSON des catégories
        chemin_categories = "categories.json"

        # Vérifie si le fichier existe
        if not os.path.exists(chemin_categories):
            self.logger.error(
                "Fichier categories.json non trouvé. "
                "Exécutez d'abord: scrapy crawl categories_spider -o categories.json"
            )
            return

        try:
            # Lit le fichier JSON des catégories
            with open(chemin_categories, 'r', encoding='utf-8') as fichier:
                categories = json.load(fichier)

            self.logger.info(f"Chargement de {len(categories)} catégories depuis {chemin_categories}")

            # Pour chaque catégorie, crée une requête
            for categorie in categories:
                nom_categorie = categorie.get('nom', 'Inconnue')
                url_complete = categorie.get('url_complete')

                if url_complete:
                    yield scrapy.Request(
                        url=url_complete,
                        callback=self.parse_category,
                        meta={'nom_categorie': nom_categorie}
                    )

        except json.JSONDecodeError as e:
            self.logger.error(f"Erreur lors de la lecture du JSON: {e}")
        except Exception as e:
            self.logger.error(f"Erreur inattendue: {e}")

    def parse_category(self, response):
        """
        Parse une page de catégorie pour extraire tous les livres

        Extrait tous les livres présents sur une page de catégorie donnée,
        puis suit les liens de pagination s'ils existent.

        Args:
            response: Réponse HTTP d'une page de catégorie

        Yields:
            dict: Données de chaque livre avec sa catégorie
            Request: Requête vers la page suivante si elle existe
        """
        # Récupère le nom de la catégorie depuis les métadonnées
        nom_categorie = response.meta.get('nom_categorie', 'Inconnue')

        # Sélectionne tous les produits (livres) sur la page
        livres = response.css("article.product_pod")

        for livre in livres:
            # Extrait les données de chaque livre
            yield {
                'categorie': nom_categorie,
                'titre': livre.css("h3 a::attr(title)").get(),
                'prix': livre.css("p.price_color::text").get(),
                'note_etoiles': livre.css("p.star-rating").attrib["class"].split()[-1],
                'url_image': response.urljoin(livre.css("div.image_container a img::attr(src)").get()),
                'url_livre': response.urljoin(livre.css("h3 a::attr(href)").get()),
                'disponibilite': self.extraire_disponibilite(livre)
            }

        # Gestion de la pagination dans chaque catégorie
        # Cherche le lien "suivant" pour continuer dans la même catégorie
        page_suivante = response.css('ul.pager li.next a::attr(href)').get()

        if page_suivante is not None:
            # Suit le lien vers la page suivante de la même catégorie
            # Transmet le nom de la catégorie via meta
            yield response.follow(
                page_suivante,
                callback=self.parse_category,
                meta={'nom_categorie': nom_categorie}
            )

    def extraire_disponibilite(self, livre):
        """
        Extrait l'information de disponibilité d'un livre

        Méthode utilitaire pour extraire et nettoyer l'information
        de disponibilité d'un produit.

        Args:
            livre: Sélecteur CSS d'un livre

        Returns:
            str: Information de disponibilité nettoyée
        """
        disponibilite = livre.css("p.instock.availability::text").getall()
        if disponibilite:
            # Joint tous les textes et nettoie les espaces
            return ' '.join(texte.strip() for texte in disponibilite if texte.strip())
        return "Information non disponible"

    def parse_book_details(self, response):
        """
        Méthode optionnelle pour extraire des détails supplémentaires

        Cette méthode peut être utilisée si on souhaite visiter chaque
        page de livre individuelle pour extraire plus d'informations
        comme la description, les métadonnées, etc.

        Args:
            response: Réponse HTTP d'une page de livre individuelle

        Yields:
            dict: Informations détaillées sur le livre
        """
        # Récupère les métadonnées transmises
        nom_categorie = response.meta.get('nom_categorie', 'Inconnue')
        infos_base = response.meta.get('infos_base', {})

        # Extrait des informations supplémentaires depuis la page du livre
        description = response.css('div#product_description + p::text').get()
        code_upc = response.css('table.table-striped tr:nth-child(1) td::text').get()
        type_produit = response.css('table.table-striped tr:nth-child(2) td::text').get()

        # Combine les informations de base avec les détails supplémentaires
        infos_detaillees = {
            **infos_base,
            'categorie': nom_categorie,
            'description': description.strip() if description else "Aucune description",
            'code_upc': code_upc,
            'type_produit': type_produit,
            'url_page': response.url
        }

        yield infos_detaillees