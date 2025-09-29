from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader


def clean_price(price_text):
    """Nettoie le prix en supprimant le symbole £"""
    if price_text:
        return float(price_text.replace('£', '').strip())
    return 0.0


def convert_star_rating(rating_class):
    """Convertit la note en étoiles en nombre"""
    if rating_class:
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        # Extrait la dernière partie de la classe CSS
        rating_word = rating_class.split()[-1] if isinstance(rating_class, str) else rating_class
        return rating_map.get(rating_word, 0)
    return 0


def convert_to_absolute_url(relative_url):
    """Convertit une URL relative en URL absolue"""
    if relative_url and relative_url.startswith('../../../'):
        return 'https://books.toscrape.com/catalogue/' + relative_url.replace('../../../', '')
    elif relative_url and not relative_url.startswith('http'):
        return 'https://books.toscrape.com/' + relative_url.lstrip('/')
    return relative_url


def convert_image_url(image_url):
    """Convertit l'URL d'image en URL absolue"""
    if image_url and image_url.startswith('../../'):
        return 'https://books.toscrape.com/' + image_url.replace('../../', '')
    elif image_url and not image_url.startswith('http'):
        return 'https://books.toscrape.com/' + image_url.lstrip('/')
    return image_url


def extract_stock_number(availability_text):
    """Extrait le nombre en stock depuis le texte de disponibilité"""
    import re
    if not availability_text:
        return 0

    # Recherche un pattern comme "(22 available)" ou "(22 disponibles)"
    match = re.search(r'\((\d+)\s*(?:available|disponibles?)?\)', str(availability_text))
    if match:
        return int(match.group(1))

    # Recherche alternative pour des patterns comme "22 available"
    match = re.search(r'(\d+)\s+(?:available|disponibles?)', str(availability_text))
    if match:
        return int(match.group(1))

    return 0


def extract_currency_symbol(price_text):
    """Extrait le symbole de devise du prix"""
    if not price_text:
        return ''

    devises = ['£', '€', '$', '¥']
    for devise in devises:
        if devise in str(price_text):
            return devise
    return ''


def clean_description(description_text):
    """Nettoie la description du livre"""
    if description_text:
        return description_text.strip()
    return "Aucune description disponible"


class BookLoader(ItemLoader):
    """ItemLoader pour traiter les données des livres"""

    default_output_processor = TakeFirst()

    # Processeurs d'entrée pour nettoyer les données
    price_in = MapCompose(clean_price)
    title_in = MapCompose(str.strip)
    star_rating_in = MapCompose(convert_star_rating)
    availability_in = MapCompose(lambda x: ' '.join(x.split()).strip())
    category_in = MapCompose(str.strip)
    url_in = MapCompose(convert_to_absolute_url)
    image_url_in = MapCompose(convert_image_url)


class BookDetailsLoader(ItemLoader):
    """ItemLoader spécialisé pour les détails complets des livres"""

    default_output_processor = TakeFirst()

    # Processeurs pour les informations de base
    titre_in = MapCompose(str.strip)
    titre_complet_in = MapCompose(str.strip)
    categorie_in = MapCompose(str.strip)
    description_in = MapCompose(clean_description)

    # Processeurs pour les prix (seulement numerique, suppression des doublons)
    prix_numerique_in = MapCompose(clean_price)

    # Processeurs pour les notes (seulement nombre, suppression texte)
    note_etoiles_nombre_in = MapCompose(convert_star_rating)

    # Processeurs pour la disponibilité (seulement tableau, suppression texte)
    nombre_stock_in = MapCompose(extract_stock_number)
    en_stock_in = MapCompose(lambda x: bool(x) if isinstance(x, bool) else str(x).lower() in ['true', '1', 'oui', 'yes', 'en stock', 'in stock'])

    # Processeurs pour les images
    url_image_in = MapCompose(convert_image_url)
    nom_fichier_image_in = MapCompose(str.strip)
    alt_image_in = MapCompose(str.strip)

    # Processeurs pour les codes et identifiants
    code_upc_in = MapCompose(str.strip)
    type_produit_in = MapCompose(str.strip)
    nombre_avis_clients_in = MapCompose(lambda x: int(x) if str(x).isdigit() else 0)
    nombre_avis_in = MapCompose(lambda x: int(x) if str(x).isdigit() else 0)

    # Processeur pour la taxe (supprime le symbole de devise)
    taxe_in = MapCompose(clean_price)