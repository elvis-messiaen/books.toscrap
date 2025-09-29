from abc import ABC, abstractstaticmethod, abstractmethod


class BookRepositoryInterface(ABC):

    """
    Recupérer tous les livres
    """
    @abstractmethod
    def get_all_books(self) -> list[dict]:
        pass

    """
    Recupérer un livre par son ID
    """

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> dict:
        pass

    """
    Sauvegarder un nouveau livre
    """
    @abstractmethod
    def save_book(self, book: dict) -> dict:
        pass

    """
    Mettre à jour un livre existant
    """
    @abstractmethod
    def update_book(self, book_id: int, book: dict) -> dict:
        pass

    """
    Supprimer un livre par son ID
    """
    @abstractmethod
    def delete_book(self, book_id: int) -> bool:
        pass
