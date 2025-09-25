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
scrapy crawl categories_spider -o categories.json && scrapy crawl books_by_categories -o books_by_categories.json
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