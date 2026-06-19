import unittest
from datetime import datetime, timezone

from app.application.shopping_list_service import ShoppingListService
from app.domain.exceptions import InvalidShoppingListError


class FakeShoppingListRepository:
    """Simula a persistência de listas de compras em memória."""

    def __init__(self):
        self.shopping_lists = []

    def add_shopping_list(self, shopping_list):
        shopping_list.list_id = len(self.shopping_lists) + 1
        self.shopping_lists.append(shopping_list)


class TestUS03ShoppingListService(unittest.TestCase):
    """US03: testa a criação de listas de compras."""

    def setUp(self):
        self.repository = FakeShoppingListRepository()
        self.created_at = datetime(
            2026,
            6,
            19,
            12,
            0,
            tzinfo=timezone.utc,
        )
        self.service = ShoppingListService(
            self.repository,
            clock=lambda: self.created_at,
        )

    def test_us03_create_shopping_list_for_user(self):
        """US03: deve associar a nova lista ao usuário informado."""
        shopping_list = self.service.create_shopping_list(
            user_id=7,
            name="Compras da semana",
        )

        self.assertEqual(shopping_list.list_id, 1)
        self.assertEqual(shopping_list.user_id, 7)
        self.assertEqual(shopping_list.name, "Compras da semana")
        self.assertEqual(shopping_list.created_at, self.created_at)
        self.assertIs(self.repository.shopping_lists[0], shopping_list)

    def test_us03_reject_empty_name_without_persisting(self):
        """US03: nome vazio deve ser rejeitado sem salvar a lista."""
        with self.assertRaises(InvalidShoppingListError):
            self.service.create_shopping_list(user_id=7, name=" ")

        self.assertEqual(self.repository.shopping_lists, [])
