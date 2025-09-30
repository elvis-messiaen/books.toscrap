# Books to Scrape - Projet Complet Scrapy + FastAPI + PostgreSQL

Projet complet combinant scraping de données avec Scrapy, base de données PostgreSQL et exposition via une API REST avec FastAPI. Ce projet extrait des données du site books.toscrape.com, les stocke en base PostgreSQL et les rend accessibles via une architecture moderne en couches.

## Architecture du Projet

### Structure Clean Architecture
```
├── main.py                     # Point d'entrée de l'API FastAPI
├── api/                        # Architecture en couches
│   ├── models/                 # Modèles de données (Book, Category)
│   │   ├── book.py            # Dataclass Book avec validation
│   │   └── category.py        # Modèle Category
│   ├── interfaces/             # Contrats d'interfaces
│   │   ├── book_repository_interface.py
│   │   ├── book_service_interface.py
│   │   ├── categories_repository_interface.py
│   │   └── categories_service_interface.py
│   ├── repositories/           # Accès aux données
│   │   ├── book_repository.py  # Repository livres (JSON → Book)
│   │   └── category_repository.py # Repository catégories
│   ├── services/              # Logique métier
│   │   ├── book_service.py    # Service livres avec validation
│   │   └── category_service.py # Service catégories
│   └── routes/                # Routes FastAPI
│       ├── books.py           # Endpoints livres (/books/*)
│       └── categories.py      # Endpoints catégories (/categories/*)
├── books_toscrape/            # Projet Scrapy
│   ├── spiders/               # Spiders de scraping
│   │   ├── books_spider.py
│   │   ├── categories_spider.py
│   │   ├── books_by_categories_spider.py
│   │   └── details_book_spider.py
│   ├── categories.json        # Données extraites
│   ├── books_by_categories.json
│   └── detail_books.json
└── requirements.txt           # Dépendances (Scrapy + FastAPI)
```

## Installation et Configuration

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

### Installation des dépendances
```bash
# Installer toutes les dépendances nécessaires (Scrapy + FastAPI)
pip install -r requirements.txt
```

### Dépendances incluses
- `scrapy` - Framework de scraping
- `fastapi` - Framework API moderne
- `uvicorn[standard]` - Serveur ASGI haute performance
- `python-multipart` - Support des formulaires
- `pydantic` - Validation de données

## Partie Scrapy - Extraction de Données

### Spiders Disponibles

#### 1. Spider des Catégories
```bash
# Extraire toutes les catégories du site
cd books_toscrape
scrapy crawl categories_spider -o categories.json
```
**Données extraites :** nom, url, url_relative

#### 2. Spider des Livres par Catégorie
```bash
# Extraire tous les livres organisés par catégorie
cd books_toscrape
scrapy crawl books_by_categories_spider -o books_by_categories.json
```
**Données extraites :** category, title, price, star_rating, image_url, url, availability

#### 3. Spider des Détails Complets
```bash
# Extraire les détails complets de chaque livre (processus long)
cd books_toscrape
scrapy crawl details_book_spider
```
**Données extraites :** 20+ champs incluant description, code UPC, taxes, livres recommandés, etc.

### Processus Complet de Scraping
```bash
# Commande complète pour extraire toutes les données
cd books_toscrape
scrapy crawl categories_spider -o categories.json && \
scrapy crawl books_by_categories_spider -o books_by_categories.json && \
scrapy crawl details_book_spider
```

### Formats d'Export Disponibles
```bash
# JSON (recommandé pour FastAPI)
scrapy crawl categories_spider -o categories.json

# CSV (pour analyse Excel)
scrapy crawl categories_spider -o categories.csv

# XML (format structuré)
scrapy crawl categories_spider -o categories.xml
```

## Partie FastAPI - API REST

### Architecture Clean Code
L'API suit les principes de Clean Architecture avec séparation claire des responsabilités :

- **Routes** : Gestion des requêtes HTTP, validation des entrées
- **Services** : Logique métier, validation des données
- **Repositories** : Accès aux données PostgreSQL et JSON
- **Models** : Structures de données typées avec Pydantic

### Lancement de l'API

#### Développement
```bash
# Lancer l'API FastAPI directement
python main.py
# Accessible sur http://localhost:8000
```

#### Alternative avec uvicorn
```bash
# Serveur de développement avec rechargement automatique
uvicorn main:app --reload
# Accessible sur http://localhost:8000
```

#### Production
```bash
# Serveur optimisé pour la production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Endpoints API Disponibles

#### Documentation
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **Schema OpenAPI** : http://localhost:8000/openapi.json

#### Endpoints Livres
```bash
# Récupérer tous les livres
GET /books/

# Récupérer un livre par ID
GET /books/{id}

# Livres par catégorie
GET /books/category/{category_name}

# Recherche avancée avec filtres
GET /books/search/?titre=harry&prix_min=10&prix_max=50&note_min=4
```

#### Endpoints Catégories
```bash
# Récupérer toutes les catégories
GET /categories/

# Récupérer une catégorie par ID
GET /categories/{id}

# Prix moyen des livres par catégorie
GET /categories/prix-moyen/

# Top des catégories par nombre de livres
GET /categories/top-nombre-livres/
```

### Exemples d'Utilisation de l'API

#### Avec cURL
```bash
# Récupérer tous les livres
curl http://localhost:8000/books/

# Récupérer un livre spécifique
curl http://localhost:8000/books/1

# Recherche par catégorie
curl http://localhost:8000/books/category/Mystery

# Recherche avec filtres multiples
curl "http://localhost:8000/books/search/?titre=sharp&prix_min=20&prix_max=60"

# Récupérer toutes les catégories
curl http://localhost:8000/categories/

# Prix moyen par catégorie
curl http://localhost:8000/categories/prix-moyen/

# Top catégories par nombre de livres
curl http://localhost:8000/categories/top-nombre-livres/
```

#### Avec Python (requests)
```python
import requests

# Récupérer tous les livres
response = requests.get("http://localhost:8000/books/")
livres = response.json()

# Recherche avec filtres
params = {"titre": "potter", "prix_max": 30}
response = requests.get("http://localhost:8000/books/search/", params=params)
resultats = response.json()

# Statistiques des catégories
response = requests.get("http://localhost:8000/categories/prix-moyen/")
prix_moyens = response.json()

response = requests.get("http://localhost:8000/categories/top-nombre-livres/")
top_categories = response.json()
```

## Fonctionnalités Avancées

### Validation Automatique
- **Pydantic Models** : Validation automatique des types de données
- **Gestion d'erreurs** : Codes HTTP appropriés (400, 404, 500)
- **Documentation automatique** : Schémas générés automatiquement

### Conversion Intelligente
- **JSON → Book** : Conversion automatique des données Scrapy vers objets typés
- **Compatibilité** : Gestion des différents noms de champs entre spiders
- **Valeurs par défaut** : Gestion gracieuse des champs manquants

### Performance
- **Architecture modulaire** : Services réutilisables et testables
- **Séparation des couches** : Repository pattern pour l'accès aux données
- **Validation métier** : Logique centralisée dans les services

## 🛠️ Développement et Tests

### Tests de Syntaxe
```bash
# Vérifier la syntaxe d'un spider
python -m py_compile books_toscrape/books_toscrape/spiders/books_spider.py

# Lister tous les spiders disponibles
cd books_toscrape
scrapy list
```

### Débogage avec Scrapy Shell
```bash
# Tester les sélecteurs interactivement
cd books_toscrape
scrapy shell "https://books.toscrape.com/index.html"
```

```python
# Dans le shell Scrapy
response.css('div.side_categories ul li ul li a::text').getall()
len(response.css('article.product_pod'))
```

### Test de l'API
```bash
# Tester la santé de l'API
curl http://localhost:8000/health

# Voir la page d'accueil avec informations
curl http://localhost:8000/
```

## Performance et Optimisation

### Scrapy
- **Spider optimisé** : Réutilisation des données entre spiders
- **Pagination automatique** : Parcours complet sans intervention
- **Gestion d'erreurs** : Reprise automatique en cas d'échec

### FastAPI
- **Serveur ASGI** : Uvicorn pour les performances maximales
- **Validation Pydantic** : Validation rapide des données
- **Documentation automatique** : Pas de maintenance supplémentaire

## Cas d'Usage

### Analyse de Données
```bash
# Extraire toutes les données pour analyse
cd books_toscrape
scrapy crawl details_book_spider

# Lancer l'API pour l'exploration interactive
python main.py
# Utiliser http://localhost:8000/docs pour explorer
```

### Intégration Frontend
```javascript
// Récupérer des livres pour une interface utilisateur
fetch('http://localhost:8000/books/')
  .then(response => response.json())
  .then(books => {
    // Afficher les livres dans l'interface
    books.forEach(book => console.log(book.title));
  });
```

### Export et Analyse
```bash
# Export CSV pour Excel
cd books_toscrape
scrapy crawl books_by_categories_spider -o livres_analyse.csv

# Puis utiliser l'API pour des requêtes spécifiques
curl "http://localhost:8000/books/search/?prix_max=25" | jq '.'
```

## Migration Future : PostgreSQL

Cette architecture est conçue pour une migration facile vers PostgreSQL :

1. **Models Book** : Mapping direct vers tables SQL
2. **Repository Pattern** : Remplacement JSON → PostgreSQL transparent
3. **Services inchangés** : Logique métier préservée
4. **Clean Architecture** : Migration par couches sans impact sur l'API

L'utilisation de dataclass `Book` au lieu de `dict` prépare parfaitement cette évolution !

## Notes Importantes

- **Temps d'exécution** : Le spider des détails peut prendre 15-30 minutes (1000+ pages)
- **Ressources** : Le scraping complet génère plusieurs MB de données JSON
- **Développement** : Utilisez `--reload` uniquement en développement
- **Production** : Configurez des workers multiples pour la performance