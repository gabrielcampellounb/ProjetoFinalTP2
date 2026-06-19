import unittest
from datetime import datetime, timezone

from app.domain.exceptions import InvalidShoppingListError
from app.domain.shopping_list import ShoppingList


class TestUS03ShoppingList(unittest.TestCase):
    """US03: testa as regras da entidade de lista de compras."""

    def test_us03_create_valid_shopping_list(self):
        """US03: deve criar lista com usuário, nome e data válidos."""
        created_at = datetime(2026, 6, 19, 12, 0, tzinfo=timezone.utc)

        shopping_list = ShoppingList(
            list_id=10,
            user_id=7,
            name="Compras da semana",
            created_at=created_at,
        )

        self.assertEqual(shopping_list.list_id, 10)
        self.assertEqual(shopping_list.user_id, 7)
        self.assertEqual(shopping_list.name, "Compras da semana")
        self.assertEqual(shopping_list.created_at, created_at)

    def test_us03_reject_empty_name(self):
        """US03: deve rejeitar nome vazio ou composto por espaços."""
        created_at = datetime.now(timezone.utc)

        for name in ("", " ", "\t\n"):
            with self.subTest(name=repr(name)):
                with self.assertRaisesRegex(
                    InvalidShoppingListError,
                    "^O nome da lista de compras não pode estar vazio\\.$",
                ):
                    ShoppingList(
                        list_id=None,
                        user_id=7,
                        name=name,
                        created_at=created_at,
                    )
