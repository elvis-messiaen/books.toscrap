# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BooksToscrapePipeline:
    def process_item(self, item, spider):
        return item

class PriceToEurosPipeline:
    """Pipeline pour convertir le prix en euros"""
## cela permet par exemple de convertir les livres sterling en euros pour un site que l'on souhaite cibler
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price = adapter.get('price', 0.0)
        if isinstance(price, (int, float)):
            # Supposons que le prix est en livres sterling et que 1 GBP = 1.16 EUR
            conversion_rate = 1.16
            adapter['price'] = round(price * conversion_rate, 2)
        return item


class PostgreSQLPipeline:
    """Pipeline pour sauvegarder directement en base PostgreSQL"""

    def __init__(self):
        self.compteur_nouveaux = 0
        self.compteur_mises_a_jour = 0

    def open_spider(self, spider):
        """Initialise la connexion à la base de données"""
        if spider.name == 'details_book_spider':
            # Import des modules nécessaires (maintenant dans le même répertoire)
            import sys
            import os

            # Ajouter le répertoire books_toscrape au chemin
            books_toscrape_dir = os.path.dirname(os.path.dirname(__file__))
            if books_toscrape_dir not in sys.path:
                sys.path.insert(0, books_toscrape_dir)

            from database_config import SessionLocal, create_tables
            from api.models.book_sql import BookSQL

            # Crée les tables si elles n'existent pas
            create_tables()

            self.session = SessionLocal()
            self.BookSQL = BookSQL
            spider.logger.info("Pipeline PostgreSQL: Connexion établie")

    def close_spider(self, spider):
        """Ferme la connexion à la base de données"""
        if spider.name == 'details_book_spider' and hasattr(self, 'session'):
            self.session.close()
            spider.logger.info(f"Pipeline PostgreSQL fermé - {self.compteur_nouveaux} nouveaux, {self.compteur_mises_a_jour} mises à jour")

    def process_item(self, item, spider):
        """Sauvegarde directement en base PostgreSQL (table propre - nouveaux livres uniquement)"""
        if spider.name != 'details_book_spider':
            return item

        adapter = ItemAdapter(item)

        try:
            # Création directe de nouveaux livres (table nettoyée)
            self.creer_nouveau_livre(adapter)
            self.compteur_nouveaux += 1
            spider.logger.info(f"PostgreSQL: Nouveau #{self.compteur_nouveaux}: {adapter.get('titre', 'Inconnu')}")

            # Commit des changements
            self.session.commit()

        except Exception as e:
            spider.logger.error(f"PostgreSQL Pipeline erreur: {e}")
            self.session.rollback()

        return item

    def creer_nouveau_livre(self, adapter):
        """Crée un nouveau livre en base"""
        import json

        nouveau_livre = self.BookSQL(
            url_page=adapter.get('url_page'),
            categorie=adapter.get('categorie'),
            title=adapter.get('titre'),  # Mapping titre -> title
            titre_complet=adapter.get('titre_complet'),
            prix_numerique=float(adapter.get('prix_numerique', 0.0)),
            note_etoiles_nombre=int(adapter.get('note_etoiles_nombre', 0)),
            nombre_avis_clients=int(adapter.get('nombre_avis_clients', 0)),
            en_stock=bool(adapter.get('en_stock', False)),
            nombre_stock=self.extraire_nombre_stock(adapter.get('nombre_stock', '')),
            description=adapter.get('description', ''),
            url_image=adapter.get('url_image'),
            nom_fichier_image=adapter.get('nom_fichier_image'),
            alt_image=adapter.get('alt_image'),
            fil_ariane=json.dumps(adapter.get('fil_ariane', []), ensure_ascii=False),
            code_upc=adapter.get('code_upc'),
            type_produit=adapter.get('type_produit', 'Books'),
            taxe=float(adapter.get('taxe', 0.0)),
            nombre_avis=int(adapter.get('nombre_avis', 0))
        )

        self.session.add(nouveau_livre)

    def mettre_a_jour_livre(self, livre_existant, adapter):
        """Met à jour un livre existant"""
        import json

        livre_existant.categorie = adapter.get('categorie')
        livre_existant.title = adapter.get('titre')  # Mapping titre -> title
        livre_existant.titre_complet = adapter.get('titre_complet')
        livre_existant.prix_numerique = float(adapter.get('prix_numerique', 0.0))
        livre_existant.note_etoiles_nombre = int(adapter.get('note_etoiles_nombre', 0))
        livre_existant.nombre_avis_clients = int(adapter.get('nombre_avis_clients', 0))
        livre_existant.en_stock = bool(adapter.get('en_stock', False))
        livre_existant.nombre_stock = self.extraire_nombre_stock(adapter.get('nombre_stock', ''))
        livre_existant.description = adapter.get('description', '')
        livre_existant.url_image = adapter.get('url_image')
        livre_existant.nom_fichier_image = adapter.get('nom_fichier_image')
        livre_existant.alt_image = adapter.get('alt_image')
        livre_existant.fil_ariane = json.dumps(adapter.get('fil_ariane', []), ensure_ascii=False)
        livre_existant.code_upc = adapter.get('code_upc')
        livre_existant.type_produit = adapter.get('type_produit', 'Books')
        livre_existant.taxe = float(adapter.get('taxe', 0.0))
        livre_existant.nombre_avis = int(adapter.get('nombre_avis', 0))

    def extraire_nombre_stock(self, nombre_stock_texte):
        """Extrait le nombre depuis le texte de stock"""
        import re

        if not nombre_stock_texte:
            return 0

        if isinstance(nombre_stock_texte, int):
            return nombre_stock_texte

        # Recherche un nombre dans le texte
        match = re.search(r'(\d+)', str(nombre_stock_texte))
        return int(match.group(1)) if match else 0


class DetailsBooksUpdatePipeline:
    """Pipeline pour gérer les mises à jour de detail_books.json avec gestion des doublons"""

    def __init__(self):
        self.fichier_sauvegarde = "detail_books.json"
        self.donnees_existantes = []
        self.index_url = {}  # Index par URL pour accès rapide
        self.nouvelles_donnees = []
        self.compteur_nouvelles = 0
        self.compteur_mises_a_jour = 0

    def open_spider(self, spider):
        """Charge les données existantes au démarrage du spider"""
        if spider.name == 'details_book_spider':
            self.charger_donnees_existantes()

    def charger_donnees_existantes(self):
        """Charge et indexe les données existantes"""
        import os
        import json

        if os.path.exists(self.fichier_sauvegarde):
            try:
                with open(self.fichier_sauvegarde, 'r', encoding='utf-8') as fichier:
                    self.donnees_existantes = json.load(fichier)

                # Crée un index par URL pour accès rapide
                for i, livre in enumerate(self.donnees_existantes):
                    url = livre.get('url_page')
                    if url:
                        self.index_url[url] = i

                print(f"Pipeline: Chargé {len(self.donnees_existantes)} livres existants")
            except json.JSONDecodeError as e:
                print(f"Pipeline: Erreur lecture JSON: {e}")
                self.donnees_existantes = []

    def process_item(self, item, spider):
        """Traite chaque item : met à jour si existe, sinon ajoute"""
        if spider.name != 'details_book_spider':
            return item

        adapter = ItemAdapter(item)
        url_page = adapter.get('url_page')

        if not url_page:
            return item

        # Convertit l'item en dictionnaire
        item_dict = dict(adapter)

        # Vérifie si l'URL existe déjà
        if url_page in self.index_url:
            # Mise à jour de l'élément existant
            index = self.index_url[url_page]
            self.donnees_existantes[index] = item_dict
            self.compteur_mises_a_jour += 1
            print(f"Pipeline: Mise à jour livre #{self.compteur_mises_a_jour}: {item_dict.get('titre', 'Inconnu')}")
        else:
            # Ajout d'un nouveau livre
            self.donnees_existantes.append(item_dict)
            self.index_url[url_page] = len(self.donnees_existantes) - 1
            self.compteur_nouvelles += 1
            print(f"Pipeline: Nouveau livre #{self.compteur_nouvelles}: {item_dict.get('titre', 'Inconnu')}")

        # Sauvegarde immédiate après chaque livre
        self.sauvegarder_donnees()

        return item

    def close_spider(self, spider):
        """Sauvegarde finale lors de la fermeture du spider"""
        if spider.name == 'details_book_spider':
            self.sauvegarder_donnees()
            print(f"Pipeline: Spider fermé - {self.compteur_nouvelles} nouveaux, {self.compteur_mises_a_jour} mises à jour")

    def sauvegarder_donnees(self):
        """Sauvegarde les données dans le fichier JSON"""
        import json

        try:
            with open(self.fichier_sauvegarde, 'w', encoding='utf-8') as fichier:
                json.dump(self.donnees_existantes, fichier, ensure_ascii=False, indent=2)
            print(f"Pipeline: Sauvegardé {len(self.donnees_existantes)} livres dans {self.fichier_sauvegarde}")
        except Exception as e:
            print(f"Pipeline: Erreur sauvegarde: {e}")
