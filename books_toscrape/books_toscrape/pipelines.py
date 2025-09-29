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
