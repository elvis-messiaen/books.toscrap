"""
Spider pour extraire les détails complets de chaque livre

Ce spider lit le fichier JSON books_by_categories.json généré par books_by_categories_spider,
puis visite chaque URL de livre pour extraire les informations détaillées.

PRÉREQUIS: Exécuter d'abord "scrapy crawl books_by_categories_spider -o books_by_categories.json"
"""
import scrapy
import json
import os

from ..items import BookDetailsProduct
from ..itemloaders import BookDetailsLoader 


class DetailsBookSpider(scrapy.Spider):
    """
    Spider pour extraire les détails complets des livres

    Ce spider lit les URLs des livres depuis books_by_categories.json
    et visite chaque page de livre pour extraire toutes les informations
    détaillées disponibles avec sauvegarde automatique en JSON.
    """
    name = "details_book_spider"
    allowed_domains = ["books.toscrape.com"]

    def __init__(self):
        """
        Initialise le spider (sauvegarde gérée par le pipeline)
        """
        super().__init__()


    def start_requests(self):
        """
        Méthode d'entrée qui lit le fichier JSON des livres par catégories

        Lit le fichier books_by_categories.json et génère une requête
        pour chaque URL de livre trouvée.

        Yields:
            Request: Requêtes vers chaque page de livre individuelle
        """
        # Chemin vers le fichier JSON des livres par catégories
        chemin_livres = "books_by_categories.json"

        # Vérifie si le fichier existe
        if not os.path.exists(chemin_livres):
            self.logger.error(
                "Fichier books_by_categories.json non trouvé. "
                "Exécutez d'abord: scrapy crawl books_by_categories_spider -o books_by_categories.json"
            )
            return

        try:
            # Lit le fichier JSON des livres
            with open(chemin_livres, 'r', encoding='utf-8') as fichier:
                livres = json.load(fichier)

            self.logger.info(f"Chargement de {len(livres)} livres depuis {chemin_livres}")

            # Pour chaque livre, crée une requête vers sa page de détails
            for livre in livres:
                url_livre = livre.get('url')

                if url_livre:
                    # FORCE le traitement de TOUTES les URLs pour permettre les mises à jour
                    yield scrapy.Request(
                        url=url_livre,
                        callback=self.parse_details_livre,
                        meta={
                            'categorie_originale': livre.get('category', 'Inconnue'),
                            'titre_original': livre.get('title', 'Inconnu')
                        }
                    )

        except json.JSONDecodeError as e:
            self.logger.error(f"Erreur lors de la lecture du JSON: {e}")
        except Exception as e:
            self.logger.error(f"Erreur inattendue: {e}")


    def parse_details_livre(self, response):
        """
        Parse une page de livre pour extraire TOUS les détails

        Extrait absolument toutes les informations disponibles
        sur la page d'un livre individuel, sans exception.

        Args:
            response: Réponse HTTP d'une page de livre

        Yields:
            dict: Données complètes du livre avec tous les détails
        """
        # Récupère les métadonnées transmises (comme fallback)
        categorie_meta = response.meta.get('categorie_originale', 'Inconnue')
        titre_original = response.meta.get('titre_original', 'Inconnu')

        # === EXTRACTION DU BREADCRUMB (FIL D'ARIANE) ===
        fil_ariane_brut = response.css('ul.breadcrumb li::text, ul.breadcrumb li a::text').getall()
        fil_ariane = [item.strip() for item in fil_ariane_brut if item and item.strip()]
        # Catégorie = avant-dernier élément du breadcrumb (le dernier est le titre du livre)
        categorie = fil_ariane[-2] if len(fil_ariane) >= 2 else categorie_meta

        # === EXTRACTION DES INFORMATIONS PRINCIPALES ===
        titre = response.css('div.product_main h1::text').get()
        prix_principal = response.css('div.product_main p.price_color::text').get()

        # === EXTRACTION DE LA NOTE EN ÉTOILES ===
        note_etoiles_classe = response.css('div.product_main p.star-rating::attr(class)').get()
        note_etoiles_nombre = self.extraire_note_etoiles(note_etoiles_classe)
        note_etoiles_texte = self.extraire_note_texte(note_etoiles_classe)

        # === EXTRACTION DE LA DISPONIBILITÉ COMPLÈTE ===
        # Disponibilité depuis la section principale
        disponibilite_principale = response.css('div.product_main p.instock.availability::text').getall()
        disponibilite_principale_texte = ' '.join([text.strip() for text in disponibilite_principale if text.strip()])

        # Statut en stock (booléen)
        en_stock = 'en stock' in disponibilite_principale_texte.lower() or 'in stock' in disponibilite_principale_texte.lower()

        # Nombre d'articles en stock
        nombre_stock = self.extraire_nombre_stock(disponibilite_principale_texte)

        # === EXTRACTION DE LA DESCRIPTION COMPLÈTE ===
        description_complete = self.extraire_description_complete(response)

        # === EXTRACTION DE L'IMAGE ===
        url_image = response.css('div#product_gallery img::attr(src)').get()
        if not url_image:
            url_image = response.css('div.item.active img::attr(src)').get()
        if url_image:
            url_image = response.urljoin(url_image)

        # Nom du fichier image
        nom_fichier_image = url_image.split('/')[-1] if url_image else None
        alt_image = response.css('div#product_gallery img::attr(alt)').get()

        # === EXTRACTION COMPLÈTE DU TABLEAU D'INFORMATIONS ===
        details_tableau_complet = self.extraire_tous_details_tableau(response)

        # === EXTRACTION DES AVIS ET ÉVALUATIONS ===
        nombre_avis_clients = details_tableau_complet.get('nombre_avis', '0')


        # === UTILISATION DU BOOKDETAILSLOADER POUR FORMATAGE AUTOMATIQUE ===
        loader = BookDetailsLoader(item=BookDetailsProduct(), response=response)

        # Informations de base
        loader.add_value('url_page', response.url)
        loader.add_value('categorie', categorie.strip() if categorie else categorie_meta)
        loader.add_css('titre', 'div.product_main h1::text')
        loader.add_css('titre_complet', 'div.product_main h1::text')

        # Prix (seulement numerique, suppression des doublons)
        loader.add_css('prix_numerique', 'div.product_main p.price_color::text')

        # Notes (seulement nombre, suppression texte)
        loader.add_css('note_etoiles_nombre', 'div.product_main p.star-rating::attr(class)')
        loader.add_value('nombre_avis_clients', details_tableau_complet.get('nombre_avis', '0'))

        # Disponibilité et stock (suppression disponibilite_texte)
        loader.add_value('en_stock', en_stock)
        loader.add_value('nombre_stock', disponibilite_principale_texte)

        # Description
        loader.add_value('description', description_complete)

        # Image
        loader.add_css('url_image', 'div#product_gallery img::attr(src)')
        if not loader.get_output_value('url_image'):
            loader.add_css('url_image', 'div.item.active img::attr(src)')
        loader.add_value('nom_fichier_image', nom_fichier_image)
        loader.add_value('alt_image', alt_image)

        # Navigation
        loader.add_value('fil_ariane', fil_ariane)

        # Détails du tableau d'informations avec processeurs automatiques
        for cle, valeur in details_tableau_complet.items():
            loader.add_value(cle, valeur)

        resultat_complet = loader.load_item()

        yield resultat_complet

    def extraire_note_etoiles(self, classe_css):
        """
        Extrait et convertit la note en étoiles en nombre

        Args:
            classe_css: Classe CSS contenant la note (ex: "star-rating Three")

        Returns:
            int: Note numérique (0-5)
        """
        if not classe_css:
            return 0

        mapping_notes = {
            'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
        }

        for mot in classe_css.split():
            if mot in mapping_notes:
                return mapping_notes[mot]
        return 0

    def convertir_prix_en_nombre(self, prix_texte):
        """
        Convertit le prix textuel en nombre

        Args:
            prix_texte: Prix sous forme de texte (ex: "£23.88")

        Returns:
            float: Prix numérique
        """
        if not prix_texte:
            return 0.0

        try:
            # Supprime le symbole de devise et convertit en float
            prix_nettoye = prix_texte.replace('£', '').replace('€', '').replace('$', '').strip()
            return float(prix_nettoye)
        except (ValueError, AttributeError):
            return 0.0

    def extraire_details_tableau(self, response):
        """
        Extrait toutes les informations du tableau de détails

        Args:
            response: Réponse HTTP de la page

        Returns:
            dict: Dictionnaire avec tous les détails du tableau
        """
        details = {}

        # Extraction des lignes du tableau
        lignes_tableau = response.css('table.table-striped tr')

        for ligne in lignes_tableau:
            cle = ligne.css('th::text').get()
            valeur = ligne.css('td::text').get()

            if cle and valeur:
                # Convertit la clé en français et nettoie
                cle_francaise = self.traduire_cle_tableau(cle.strip())
                details[cle_francaise] = valeur.strip()

        return details

    def traduire_cle_tableau(self, cle_anglaise):
        """
        Traduit les clés du tableau en français (méthode legacy)
        Utilisez traduire_et_nettoyer_cle() pour la version complète

        Args:
            cle_anglaise: Clé en anglais

        Returns:
            str: Clé traduite en français
        """
        return self.traduire_et_nettoyer_cle(cle_anglaise)

    def extraire_nombre_stock(self, disponibilite_texte):
        """
        Extrait le nombre d'articles en stock depuis le texte de disponibilité

        Args:
            disponibilite_texte: Texte de disponibilité (ex: "In stock (22 available)")

        Returns:
            int: Nombre d'articles en stock, 0 si non trouvé
        """
        import re

        if not disponibilite_texte:
            return 0

        # Recherche un pattern comme "(22 available)" ou "(22)"
        match = re.search(r'\((\d+)\s*(?:available)?\)', disponibilite_texte)
        if match:
            return int(match.group(1))

        # Recherche alternative pour des patterns comme "22 available"
        match = re.search(r'(\d+)\s+available', disponibilite_texte)
        if match:
            return int(match.group(1))

        return 0

    def extraire_description_complete(self, response):
        """
        Extrait la description complète du livre depuis la page

        Args:
            response: Réponse HTTP de la page

        Returns:
            str: Description complète du livre
        """
        # Méthode principale: description après le titre "Description du produit"
        description = response.css('div#product_description + p::text').get()

        if not description:
            # Méthode alternative: chercher après h2 contenant "Description"
            description = response.xpath('//h2[contains(text(), "Description")]/following-sibling::p[1]/text()').get()

        if not description:
            # Méthode alternative: chercher dans les paragraphes après product_description
            description = response.css('div#product_description').xpath('following-sibling::p[1]/text()').get()

        if not description:
            # Dernière alternative: chercher tout paragraphe contenant du texte substantiel
            paragraphes = response.css('article.product_page p::text').getall()
            for p in paragraphes:
                if p and len(p.strip()) > 50:  # Description substantielle
                    description = p
                    break

        return description.strip() if description else "Aucune description disponible"

    def extraire_tous_details_tableau(self, response):
        """
        Extrait les détails du tableau d'informations produit (exclusion des champs redondants)

        Args:
            response: Réponse HTTP de la page

        Returns:
            dict: Dictionnaire avec les détails du tableau (sans doublons)
        """
        details = {}
        champs_a_exclure = ['prix_hors_taxe', 'prix_avec_taxe', 'disponibilite_tableau']

        # Extraction des lignes du tableau d'informations produit
        lignes_tableau = response.css('table.table-striped tr')

        for ligne in lignes_tableau:
            cle = ligne.css('th::text').get()
            valeur = ligne.css('td::text').get()

            if cle and valeur:
                # Nettoie et traduit la clé
                cle_francaise = self.traduire_et_nettoyer_cle(cle.strip())

                # Ignore les champs redondants
                if cle_francaise in champs_a_exclure:
                    continue

                valeur_nettoyee = valeur.strip()

                # Stocke la valeur brute et traitée
                details[cle_francaise] = valeur_nettoyee

                # Traitement spécial pour certains champs (sauf ceux exclus)
                if 'prix' in cle_francaise.lower() and cle_francaise not in champs_a_exclure:
                    details[f"{cle_francaise}_numerique"] = self.convertir_prix_en_nombre(valeur_nettoyee)

        return details

    def traduire_et_nettoyer_cle(self, cle_anglaise):
        """
        Traduit et nettoie les clés du tableau en français

        Args:
            cle_anglaise: Clé en anglais depuis le tableau

        Returns:
            str: Clé traduite et nettoyée en français
        """
        traductions = {
            'UPC': 'code_upc',
            'Product Type': 'type_produit',
            'Price (excl. tax)': 'prix_hors_taxe',
            'Price (incl. tax)': 'prix_avec_taxe',
            'Tax': 'taxe',
            'Availability': 'disponibilite_tableau',
            'Number of reviews': 'nombre_avis',
            'Code UPC': 'code_upc',
            'Type de produit': 'type_produit',
            'Prix ​​(hors taxes)': 'prix_hors_taxe',
            'Prix ​​(TTC)': 'prix_avec_taxe',
            'Impôt': 'taxe',
            'Disponibilité': 'disponibilite_tableau',
            'Nombre d\'avis': 'nombre_avis'
        }

        return traductions.get(cle_anglaise, cle_anglaise.lower().replace(' ', '_').replace('​', ''))

    def extraire_note_texte(self, note_classe):
        """
        Extrait la note en texte depuis la classe CSS

        Args:
            note_classe: Classe CSS contenant la note

        Returns:
            str: Note en texte (One, Two, Three, Four, Five)
        """
        if not note_classe:
            return "Non noté"

        mots_notes = ['One', 'Two', 'Three', 'Four', 'Five']
        for mot in note_classe.split():
            if mot in mots_notes:
                return mot
        return "Non noté"

    def extraire_devise(self, prix_texte):
        """
        Extrait le symbole de devise du prix

        Args:
            prix_texte: Prix sous forme de texte

        Returns:
            str: Symbole de devise
        """
        if not prix_texte:
            return ''

        devises = ['£', '€', '$', '¥']
        for devise in devises:
            if devise in prix_texte:
                return devise
        return ''
