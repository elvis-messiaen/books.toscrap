from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    name: str
    url = str

    id: Optional[int] = None