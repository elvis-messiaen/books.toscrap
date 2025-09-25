"""
Spider pour extraire toutes les catégories de livres disponibles sur books.toscrape.com

Ce spider parcourt la page d'accueil et extrait :
- Le nom de chaque catégorie
- L'URL de la catégorie
- Le nombre de livres dans la catégorie (si disponible)
"""
import scrapy


class CategoriesSpiderSpider(scrapy.Spider):
    """
    Spider dédié à l'extraction des catégories de livres

    Utilise la page d'accueil comme point de départ pour découvrir
    toutes les catégories disponibles sur le site
    """
    name = "categories_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/index.html"]

    def parse(self, response):
        """
        Méthode principale pour extraire les catégories

        Parcourt le menu latéral des catégories et extrait les informations
        de chaque catégorie disponible

        Args:
            response: Réponse HTTP de la page d'accueil

        Yields:
            dict: Dictionnaire contenant les informations de chaque catégorie
        """
        # Sélectionne tous les liens de catégories dans le menu latéral
        liens_categories = response.css('div.side_categories ul li ul li a')

        for lien in liens_categories:
            # Extrait le nom de la catégorie (texte du lien)
            nom_categorie = lien.css('::text').get()

            # Extrait l'URL relative de la catégorie
            url_relative_categorie = lien.css('::attr(href)').get()

            # Convertit l'URL relative en URL absolue
            url_complete = response.urljoin(url_relative_categorie)

            # Nettoie le nom de la catégorie (supprime les espaces)
            if nom_categorie:
                nom_categorie = nom_categorie.strip()

            # Retourne les données de la catégorie
            yield {
                'nom': nom_categorie,
                'url_complete': url_complete,
                'url_relative': url_relative_categorie
            }

    def parse_category_details(self, response):
        """
        Méthode optionnelle pour extraire des détails supplémentaires
        sur chaque catégorie (nombre de livres, etc.)

        Cette méthode peut être utilisée si on souhaite visiter chaque
        page de catégorie pour extraire plus d'informations

        Args:
            response: Réponse HTTP de la page d'une catégorie

        Yields:
            dict: Informations détaillées sur la catégorie
        """
        # Trouve le nombre total de résultats pour cette catégorie
        texte_resultats = response.css('form strong::text').get()

        if texte_resultats:
            # Extrait le nombre de livres dans la catégorie
            nombre_livres = texte_resultats.strip()
        else:
            nombre_livres = "Non disponible"

        # Extrait le nom de la catégorie depuis le breadcrumb
        nom_categorie = response.css('ul.breadcrumb li:last-child::text').get()

        if nom_categorie:
            nom_categorie = nom_categorie.strip()

        yield {
            'nom_categorie': nom_categorie,
            'nombre_livres': nombre_livres,
            'url_page': response.url
        }