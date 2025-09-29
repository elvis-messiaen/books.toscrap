# Books to Scrape - Projet de Scraping avec Scrapy

Ce projet utilise Scrapy pour extraire des données du site books.toscrape.com

## Commandes disponibles

### Installation et configuration

```bash
# Installe toutes les dépendances nécessaires au projet
# Nécessaire avant de pouvoir lancer le scraper
pip install -r requirements.txt
```

### Lancement du scraper

```bash
# Lance le spider "books_spider" pour extraire les données des livres
# Collecte les informations comme le titre, prix, notation et URLs des livres
cd books_toscrape
scrapy crawl books_spider
```

```bash
# Lance le scraper et sauvegarde les résultats dans un fichier JSON
# Utile pour conserver les données extraites dans un format structuré
cd books_toscrape
scrapy crawl books_spider -o books.json
```

```bash
# Lance le scraper et sauvegarde les résultats dans un fichier CSV
# Format pratique pour analyser les données dans Excel ou autres outils
cd books_toscrape
scrapy crawl books_spider -o books.csv
```

### Vérification et tests

```bash
# Vérifie la syntaxe Python du spider principal
# Permet de détecter les erreurs de syntaxe avant l'exécution
python -m py_compile books_toscrape/books_toscrape/spiders/books_spider.py
```

```bash
# Liste tous les spiders disponibles dans le projet
# Utile pour vérifier que le spider est bien configuré
cd books_toscrape
scrapy list
```

### Débogage et développement

```bash
# Lance Scrapy shell pour tester les sélecteurs CSS/XPath
# Permet de tester interactivement l'extraction de données
cd books_toscrape
scrapy shell "https://books.toscrape.com/catalogue/category/books_1/index.html"
```

```bash
# Affiche des informations détaillées sur le projet Scrapy
# Utile pour vérifier la configuration du projet
cd books_toscrape
scrapy settings --get=BOT_NAME
```

## Structure du projet

- `books_toscrape/` : Répertoire principal du projet Scrapy
- `books_toscrape/spiders/books_spider.py` : Spider principal qui extrait les données des livres
- `books_toscrape/spiders/categories_spider.py` : Spider pour extraire les catégories de livres
- `books_toscrape/spiders/books_by_categories_spider.py` : Spider pour extraire les livres organisés par catégorie
- `books_toscrape/spiders/details_book_spider.py` : Spider pour extraire les détails complets de chaque livre
- `requirements.txt` : Liste des dépendances Python

## Fonctionnalités du Spider

Le spider `books_spider` extrait les données suivantes pour chaque livre :
- **title** : Titre du livre
- **price** : Prix du livre
- **star_rating** : Note en étoiles (One, Two, Three, Four, Five)
- **image_url** : URL de l'image de couverture
- **url** : URL de la page détaillée du livre

### Navigation automatique entre les pages
Le spider utilise la pagination automatique pour parcourir toutes les pages de livres :
```python
# Recherche le lien "suivant" pour continuer sur les autres pages
next_page = response.css('ul.pager li.next a::attr(href)').get()
if next_page is not None:
    yield response.follow(next_page_url, callback=self.parse)
```

## Formats d'export disponibles

```bash
# Export en JSON (format structuré pour les APIs)
cd books_toscrape
scrapy crawl books_spider -o books.json

# Export en CSV (compatible Excel/tableur)
cd books_toscrape
scrapy crawl books_spider -o books.csv

# Export en XML (format structuré standard)
cd books_toscrape
scrapy crawl books_spider -o books.xml

# Export en JSONLINES (une ligne JSON par item)
cd books_toscrape
scrapy crawl books_spider -o books.jl
```

## Test et débogage avec Scrapy Shell

```bash
# Lance le shell interactif pour tester les sélecteurs
cd books_toscrape
scrapy shell "https://books.toscrape.com/catalogue/category/books_1/index.html"
```

Dans le shell Scrapy, vous pouvez tester :
```python
# Tester l'extraction des produits
products = response.css("article.product_pod")
len(products)  # Nombre de produits sur la page

# Tester l'extraction d'un titre
product = products[0]
product.css("h3 a::attr(title)").get()

# Tester la pagination
next_page = response.css('ul.pager li.next a::attr(href)').get()
print(next_page)
```

## Spider des Catégories

Le spider `categories_spider` extrait toutes les catégories disponibles sur le site :

### Commandes pour le spider des catégories

```bash
# Lance le spider pour extraire toutes les catégories
cd books_toscrape
scrapy crawl categories_spider

# Export des catégories en JSON
cd books_toscrape
scrapy crawl categories_spider -o categories.json

# Export des catégories en CSV
cd books_toscrape
scrapy crawl categories_spider -o categories.csv
```

### Données extraites par categories_spider

- **name** : Nom de la catégorie (ex: "Travel", "Mystery", "Romance")
- **url** : URL complète de la catégorie
- **relative_url** : URL relative de la catégorie

### Test du spider des catégories

```bash
# Tester les sélecteurs de catégories avec Scrapy Shell
cd books_toscrape
scrapy shell "https://books.toscrape.com/index.html"
```

Dans le shell, vous pouvez tester :
```python
# Extraire tous les liens de catégories
category_links = response.css('div.side_categories ul li ul li a')
len(category_links)  # Nombre total de catégories

# Tester l'extraction du premier lien
first_link = category_links[0]
first_link.css('::text').get()  # Nom de la catégorie
first_link.css('::attr(href)').get()  # URL relative
```

## Spider des Livres par Catégorie

Le spider `books_by_categories` combine les fonctionnalités des deux autres spiders pour extraire tous les livres du site organisés par catégorie :

### Fonctionnement du spider books_by_categories (Optimisé)

1. **Lecture du JSON** : Lit le fichier `categories.json` généré par `categories_spider`
2. **Parcours par catégorie** : Visite chaque page de catégorie depuis le JSON
3. **Extraction complète** : Pour chaque catégorie, extrait tous les livres avec pagination automatique
4. **Association catégorie-livre** : Chaque livre est associé à sa catégorie d'origine

### Avantages de l'optimisation

- **Plus rapide** : Évite le double scrapping des catégories
- **Plus efficace** : Réutilise les données déjà extraites
- **Plus modulaire** : Séparation claire des responsabilités
- **Économie de bande passante** : Moins de requêtes HTTP

### Commandes pour le spider des livres par catégorie

**PRÉREQUIS IMPORTANT** : Ce spider optimisé lit le fichier des catégories au lieu de les re-scrapper.

```bash
# ÉTAPE 1: Générer d'abord le fichier des catégories (rapide)
cd books_toscrape
scrapy crawl categories_spider -o categories.json

# ÉTAPE 2: Lancer le spider des livres par catégorie (utilise le JSON)
cd books_toscrape
scrapy crawl books_by_categories -o books_by_categories.json

# Export en CSV pour analyse dans Excel
cd books_toscrape
scrapy crawl books_by_categories -o books_by_categories.csv
```

### Commandes combinées (automatisées)

```bash
# Commande complète : catégories + livres par catégorie en une fois
cd books_toscrape
scrapy crawl categories_spider -o categories.json && scrapy crawl books_by_categories_spider -o books_by_categories.json
```

### Écrasement des fichiers existants

```bash
# Pour écraser un fichier existant au lieu de l'ajouter (utiliser -O majuscule)
cd books_toscrape
scrapy crawl books_by_categories_spider -O books_by_categories.json
```

### Données extraites par books_by_categories

- **category** : Nom de la catégorie du livre (ex: "Travel", "Mystery", "Fiction")
- **title** : Titre du livre
- **price** : Prix du livre
- **star_rating** : Note en étoiles (One, Two, Three, Four, Five)
- **image_url** : URL de l'image de couverture
- **url** : URL de la page détaillée du livre
- **availability** : Information de disponibilité du livre

### Avantages de ce spider

- **Organisation par catégorie** : Facilite l'analyse des données par genre littéraire
- **Couverture complète** : Assure qu'aucun livre n'est manqué grâce au parcours systématique
- **Données enrichies** : Chaque livre inclut sa catégorie d'appartenance
- **Pagination automatique** : Gère automatiquement toutes les pages de chaque catégorie

### Performance et utilisation

**Note importante** : Ce spider parcourt l'intégralité du site (50+ catégories, 1000+ livres). L'exécution complète peut prendre plusieurs minutes.

```bash
# Pour tester sur une catégorie spécifique, utilisez Scrapy Shell
cd books_toscrape
scrapy shell "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
```

### Exemple de données extraites

```json
{
  "category": "Mystery",
  "title": "Sharp Objects",
  "price": "£47.82",
  "star_rating": "Four",
  "image_url": "https://books.toscrape.com/media/cache/32/51/...",
  "url": "https://books.toscrape.com/catalogue/sharp-objects_997/index.html",
  "availability": "In stock (20 available)"
}
```

## Spider des Détails de Livres

Le spider `details_book` extrait les informations complètes de chaque livre en visitant individuellement chaque page de livre :

### Fonctionnement du spider details_book

1. **Lecture du JSON** : Lit le fichier `books_by_categories.json` pour récupérer les URLs des livres
2. **Visite individuelle** : Visite chaque page de livre pour extraire les détails complets
3. **Extraction enrichie** : Collecte toutes les informations disponibles (description, tableau de détails, etc.)
4. **Variables en français** : Toutes les variables sont nommées en français

### Commandes pour le spider des détails

**PRÉREQUIS IMPORTANT** : Ce spider nécessite le fichier `books_by_categories.json`.

```bash
# ÉTAPE 1: Générer d'abord les livres par catégorie
cd books_toscrape
scrapy crawl books_by_categories_spider -o books_by_categories.json

# ÉTAPE 2: Extraire les détails complets de chaque livre (sauvegarde automatique)
cd books_toscrape
scrapy crawl details_book_spider

# Le fichier detail_books.json est créé/mis à jour automatiquement
# Pas besoin de spécifier -o, la sauvegarde est intégrée au spider
```

### Données extraites par details_book

- **url_page** : URL de la page du livre
- **categorie** : Catégorie du livre (extraite depuis le breadcrumb)
- **titre** : Titre complet du livre
- **prix_original** : Prix avec symbole de devise
- **prix_numerique** : Prix converti en nombre
- **note_etoiles** : Note en nombre (1-5)
- **disponibilite** : Information de disponibilité complète
- **nombre_stock** : Nombre d'articles en stock (extrait de la disponibilité)
- **description** : Description complète du livre
- **url_image** : URL de l'image haute résolution
- **fil_ariane** : Chemin de navigation (breadcrumb)
- **code_upc** : Code produit unique
- **type_produit** : Type de produit
- **prix_hors_taxe** : Prix hors taxes
- **prix_avec_taxe** : Prix taxes comprises
- **taxe** : Montant des taxes
- **nombre_avis** : Nombre d'avis clients
- **livres_recommandes** : Liste des livres similaires (exclut les produits consultés)

### Commandes combinées complètes

```bash
# Processus complet : catégories → livres par catégorie → détails
cd books_toscrape
scrapy crawl categories_spider -o categories.json && scrapy crawl books_by_categories_spider -o books_by_categories.json && scrapy crawl details_book_spider -o details_livres.json
```

### Performance et utilisation

**Note importante** : Ce spider visite CHAQUE page de livre individuellement (1000+ pages). L'exécution peut prendre 15-30 minutes selon la configuration réseau.

### Exemple de données détaillées extraites

```json
{
  "url_page": "https://books.toscrape.com/catalogue/sharp-objects_997/index.html",
  "categorie": "Mystery",
  "titre": "Sharp Objects",
  "prix_original": "£47.82",
  "prix_numerique": 47.82,
  "note_etoiles": 4,
  "disponibilite": "In stock (20 available)",
  "nombre_stock": 20,
  "description": "WICKED above her hipbone, GIRL across her heart...",
  "url_image": "https://books.toscrape.com/media/cache/32/51/...",
  "fil_ariane": ["Home", "Books", "Mystery"],
  "code_upc": "90fa61229261140a",
  "type_produit": "Books",
  "prix_hors_taxe": "47.82",
  "prix_avec_taxe": "47.82",
  "taxe": "0.00",
  "nombre_avis": "0",
  "livres_recommandes": ["The Girl with the Dragon Tattoo", "Gone Girl"]
}
```

## API FastAPI - Serveur de données

Ce projet intègre un serveur FastAPI pour exposer les données scrapées via une API REST moderne et performante.

### Installation des dépendances FastAPI

```bash
# Installer FastAPI et Uvicorn (serveur ASGI)
pip install fastapi uvicorn python-multipart
```

### Lancement du serveur FastAPI

```bash
# Lancer le serveur de développement avec rechargement automatique
# Le serveur sera accessible sur http://localhost:8000
uvicorn main:app --reload

# Lancer le serveur en production sur un port spécifique
uvicorn main:app --host 0.0.0.0 --port 8000

# Lancer le serveur avec des workers multiples (production)
uvicorn main:app --workers 4
```

### Endpoints API disponibles

L'API FastAPI fournit les endpoints suivants pour accéder aux données scrapées :

```bash
# Documentation interactive Swagger UI
http://localhost:8000/docs

# Documentation ReDoc alternative
http://localhost:8000/redoc

# API Schema OpenAPI
http://localhost:8000/openapi.json
```

### Fonctionnalités de l'API

- **CRUD complet** : Création, lecture, mise à jour et suppression des données de livres
- **Filtrage avancé** : Recherche par catégorie, prix, note, disponibilité
- **Pagination** : Navigation efficace dans les grandes collections de données
- **Validation automatique** : Validation des données entrantes avec Pydantic
- **Documentation interactive** : Interface Swagger UI intégrée
- **Support JSON** : Lecture et écriture des fichiers JSON générés par Scrapy

### Sources de données

L'API FastAPI lit et manipule les fichiers JSON suivants générés par les spiders Scrapy :

- `books_toscrape/categories.json` : Données des catégories de livres
- `books_toscrape/books_by_categories.json` : Livres organisés par catégorie
- `books_toscrape/detail_books.json` : Détails complets de chaque livre
- `books_toscrape/mydara.json` : Données personnalisées

### Exemples d'utilisation de l'API

```bash
# Récupérer tous les livres
curl http://localhost:8000/books

# Récupérer un livre par ID
curl http://localhost:8000/books/1

# Récupérer les livres d'une catégorie
curl http://localhost:8000/books/category/Mystery

# Rechercher des livres par prix
curl "http://localhost:8000/books?price_min=10&price_max=50"

# Récupérer les statistiques
curl http://localhost:8000/stats
```
```