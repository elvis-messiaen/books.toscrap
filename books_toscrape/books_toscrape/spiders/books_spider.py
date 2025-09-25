"""
Spider pour extraire tous les livres du site books.toscrape.com

Ce spider parcourt toutes les pages de livres et extrait les informations
de base de chaque livre avec pagination automatique.
"""
import scrapy


class BooksSpiderSpider(scrapy.Spider):
    """
    Spider principal pour l'extraction de tous les livres

    Utilise la pagination pour parcourir l'ensemble du catalogue
    de livres disponibles sur le site.
    """
    name = "books_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books_1/index.html"]

    def parse(self, response):
        """
        Méthode principale pour extraire les livres d'une page

        Parcourt tous les livres présents sur une page et suit
        les liens de pagination pour continuer sur les pages suivantes.

        Args:
            response: Réponse HTTP de la page courante

        Yields:
            dict: Données de chaque livre trouvé sur la page
        """
        # Sélectionne tous les articles de livres sur la page
        livres = response.css("article.product_pod")

        for livre in livres:
            yield {
                'titre': livre.css("h3 a::attr(title)").get(),
                'prix': livre.css("p.price_color::text").get(),
                'note_etoiles': livre.css("p.star-rating").attrib["class"].split()[-1],
                'url_image': response.urljoin(livre.css("div.image_container a img::attr(src)").get()),
                'url_livre': response.urljoin(livre.css("h3 a::attr(href)").get()),
            }

        # Recherche le lien vers la page suivante
        page_suivante = response.css('ul.pager li.next a::attr(href)').get()

        if page_suivante is not None:
            # Construction de l'URL complète de la page suivante
            url_page_suivante = 'https://books.toscrape.com/catalogue/' + page_suivante
            yield response.follow(url_page_suivante, callback=self.parse)
