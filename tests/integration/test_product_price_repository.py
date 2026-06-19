import sqlite3
import unittest
from datetime import datetime

from app.domain.product_price import ProductPrice
from app.infrastructure.product_price_repository import (
    SQLiteProductPriceRepository,
)


class TestUS06SQLiteProductPriceRepository(unittest.TestCase):
    """US06: testa o histórico SQLite de preços por produto e local."""

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.repository = SQLiteProductPriceRepository(self.connection)
        self.repository.create_table()

    def tearDown(self):
        self.connection.close()

    def test_us06_add_and_list_product_price_history(self):
        """US06: deve preservar vários preços observados para um produto."""
        older_price = ProductPrice(
            product_bar_code="1234567890123",
            store_id=2,
            user_id=7,
            price=9.50,
            created_at=datetime(2026, 6, 18, 10, 30),
        )
        newer_price = ProductPrice(
            product_bar_code="1234567890123",
            store_id=3,
            user_id=8,
            price=8.75,
            created_at=datetime(2026, 6, 19, 11, 45),
        )

        self.repository.add_price(older_price)
        self.repository.add_price(newer_price)
        prices = self.repository.list_prices_by_product("1234567890123")

        self.assertEqual(len(prices), 2)
        self.assertEqual(prices[0].store_id, 3)
        self.assertEqual(prices[0].user_id, 8)
        self.assertEqual(prices[0].price, 8.75)
        self.assertEqual(prices[0].created_at, datetime(2026, 6, 19, 11, 45))
        self.assertEqual(prices[1].store_id, 2)

    def test_us06_list_prices_only_for_requested_product(self):
        """US06: consulta não deve misturar históricos de produtos distintos."""
        self.repository.add_price(
            ProductPrice(
                product_bar_code="1234567890123",
                store_id=2,
                user_id=7,
                price=9.50,
                created_at=datetime(2026, 6, 18, 10, 30),
            )
        )
        self.repository.add_price(
            ProductPrice(
                product_bar_code="9876543210123",
                store_id=2,
                user_id=7,
                price=5.25,
                created_at=datetime(2026, 6, 19, 10, 30),
            )
        )

        prices = self.repository.list_prices_by_product("1234567890123")

        self.assertEqual(len(prices), 1)
        self.assertEqual(prices[0].product_bar_code, "1234567890123")
