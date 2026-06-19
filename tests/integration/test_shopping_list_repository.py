import sqlite3
import unittest
from datetime import datetime, timezone

from app.domain.shopping_list import ShoppingList
from app.infrastructure.shopping_list_repository import (
    SQLiteShoppingListRepository,
)


class TestUS03SQLiteShoppingListRepository(unittest.TestCase):
    """US03: testa a persistência SQLite de listas de compras."""

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.repository = SQLiteShoppingListRepository(self.connection)
        self.repository.create_table()

    def tearDown(self):
        self.connection.close()

    def test_us03_add_and_get_shopping_list(self):
        """US03: deve persistir lista associada ao usuário."""
        created_at = datetime(2026, 6, 19, 12, 0, tzinfo=timezone.utc)
        shopping_list = ShoppingList(
            list_id=None,
            user_id=7,
            name="Compras da semana",
            created_at=created_at,
        )

        self.repository.add_shopping_list(shopping_list)
        stored_list = self.repository.get_shopping_list_by_id(
            shopping_list.list_id
        )

        self.assertIsInstance(shopping_list.list_id, int)
        self.assertEqual(stored_list.user_id, 7)
        self.assertEqual(stored_list.name, "Compras da semana")
        self.assertEqual(stored_list.created_at, created_at)
