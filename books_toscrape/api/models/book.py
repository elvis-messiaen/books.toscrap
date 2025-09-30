from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    id: Optional[int] = None
    url_page: str = ""
    categorie: str = ""
    title: str = ""
    prix_numerique: float = 0.0
    note_etoiles_nombre: int = 0
    nombre_avis_clients: int = 0
    en_stock: bool = False
    nombre_stock: int = 0
    description: str = ""
    url_image: str = ""
    nom_fichier_image: str = ""
    alt_image: str = ""
    fil_ariane: str = ""
    code_upc: str = ""
    type_produit: str = "Books"
    taxe: float = 0.0
    nombre_avis: int = 0