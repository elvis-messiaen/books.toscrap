# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksToscrapeProduct(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    star_rating = scrapy.Field()
    image_url = scrapy.Field()
    url = scrapy.Field()
    availability = scrapy.Field()


class BookDetailsProduct(scrapy.Item):
    """Item pour les détails complets des livres"""
    # Informations de base
    url_page = scrapy.Field()
    categorie = scrapy.Field()
    titre = scrapy.Field()
    titre_complet = scrapy.Field()

    # Prix et informations financières
    prix_affiche = scrapy.Field()
    prix_numerique = scrapy.Field()
    devise = scrapy.Field()

    # Notes et évaluations
    note_etoiles_nombre = scrapy.Field()
    note_etoiles_texte = scrapy.Field()
    nombre_avis_clients = scrapy.Field()

    # Disponibilité et stock
    disponibilite_texte = scrapy.Field()
    en_stock = scrapy.Field()
    nombre_stock = scrapy.Field()

    # Description
    description = scrapy.Field()

    # Image
    url_image = scrapy.Field()
    nom_fichier_image = scrapy.Field()
    alt_image = scrapy.Field()

    # Navigation
    fil_ariane = scrapy.Field()

    # Détails du tableau d'informations
    code_upc = scrapy.Field()
    type_produit = scrapy.Field()
    prix_hors_taxe = scrapy.Field()
    prix_hors_taxe_numerique = scrapy.Field()
    prix_avec_taxe = scrapy.Field()
    prix_avec_taxe_numerique = scrapy.Field()
    taxe = scrapy.Field()
    taxe_numerique = scrapy.Field()
    disponibilite_tableau = scrapy.Field()
    nombre_avis = scrapy.Field()