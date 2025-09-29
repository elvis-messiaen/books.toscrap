from abc import ABC, abstractmethod


class BookServiceInterface(ABC):

    """
    récupérer tous les livres
    """
    @abstractmethod
    def get_all_books(self) -> list[dict]:
        pass

    """
    récupérer un livre par son ID
    """
    @abstractmethod
    def get_book_by_id(self, book_id: int) -> dict:
        pass

    """
    créer un nouveau livre avec validation métier
    """
    @abstractmethod
    def create_book(self, book_data: dict) -> dict:
        pass

    """
    mettre à jour un livre existant
    """
    @abstractmethod
    def update_book(self, book_id: int, book_data: dict) -> dict:
        pass

    """
    supprimer un livre par son ID
    """
    @abstractmethod
    def delete_book(self, book_id: int) -> bool:
        pass
