import re
import sqlite3
import unittest

from app.domain.exceptions import DuplicateBarcodeError, InvalidQuantityError
from app.domain.product import Product
from app.infrastructure.product_repository import SQLiteProductRepository


class TestSQLiteProductRepository(unittest.TestCase):
    """Testa a persistência real de produtos em SQLite."""

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.repository = SQLiteProductRepository(self.connection)
        self.repository.create_table()

    def tearDown(self):
        self.connection.close()

    @staticmethod
    def create_product(
        bar_code="1234567890123",
        name="Produto de teste",
    ):
        """Cria um produto válido para os testes do repositório."""
        return Product(
            name=name,
            brand="Marca de teste",
            price=9.99,
            bar_code=bar_code,
        )

    def test_add_and_get_product(self):
        """Deve salvar e recuperar produto e quantidade."""
        product = self.create_product()

        self.repository.add_product(product, quantity=10)
        stored_product, stored_quantity = (
            self.repository.get_product_by_bar_code(product.bar_code)
        )

        self.assertEqual(stored_product.name, "Produto de teste")
        self.assertEqual(stored_product.brand, "Marca de teste")
        self.assertEqual(stored_product.price, 9.99)
        self.assertEqual(stored_product.bar_code, "1234567890123")
        self.assertEqual(stored_quantity, 10)

    def test_get_missing_product(self):
        """Deve retornar None quando o produto não existir."""
        result = self.repository.get_product_by_bar_code("9999999999999")

        self.assertIsNone(result)

    def test_add_product_with_zero_quantity(self):
        """Deve persistir um produto com estoque zero."""
        product = self.create_product()

        self.repository.add_product(product, quantity=0)
        _, stored_quantity = self.repository.get_product_by_bar_code(
            product.bar_code
        )

        self.assertEqual(stored_quantity, 0)

    def test_reject_invalid_quantity(self):
        """Deve rejeitar quantidades inválidas sem inserir registros."""
        invalid_cases = (
            (-1, "A quantidade do produto não pode ser negativa."),
            (1.5, "A quantidade do produto deve ser um número inteiro."),
            ("5", "A quantidade do produto deve ser um número inteiro."),
            (True, "A quantidade do produto deve ser um número inteiro."),
            (None, "A quantidade do produto deve ser um número inteiro."),
            ([], "A quantidade do produto deve ser um número inteiro."),
        )

        for quantity, message in invalid_cases:
            product = self.create_product()

            with self.subTest(quantity=quantity):
                with self.assertRaisesRegex(
                    InvalidQuantityError,
                    f"^{re.escape(message)}$",
                ):
                    self.repository.add_product(product, quantity=quantity)

                self.assertIsNone(
                    self.repository.get_product_by_bar_code(product.bar_code)
                )

    def test_reject_duplicate_bar_code(self):
        """Deve rejeitar duplicidade e preservar o registro original."""
        original_product = self.create_product(name="Produto original")
        duplicate_product = self.create_product(name="Produto duplicado")
        self.repository.add_product(original_product, quantity=10)

        with self.assertRaisesRegex(
            DuplicateBarcodeError,
            "^Já existe um produto com o código de barras 1234567890123\\.$",
        ):
            self.repository.add_product(duplicate_product, quantity=20)

        stored_product, stored_quantity = (
            self.repository.get_product_by_bar_code(original_product.bar_code)
        )
        record_count = self.connection.execute(
            "SELECT COUNT(*) FROM products;"
        ).fetchone()[0]

        self.assertEqual(stored_product.name, "Produto original")
        self.assertEqual(stored_quantity, 10)
        self.assertEqual(record_count, 1)
