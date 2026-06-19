import sqlite3
import unittest

from app.application.product_service import ProductService
from app.web.dependencies import initialize_product_service


class TestAD01WebDependencies(unittest.TestCase):
    """AD01: testa a composição das dependências da camada web."""

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")

    def tearDown(self):
        self.connection.close()

    def test_ad01_initialize_product_service(self):
        """AD01: deve criar tabela, repositório e serviço de produtos."""
        product_service = initialize_product_service(self.connection)

        table = self.connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'products';
            """
        ).fetchone()

        self.assertIsInstance(product_service, ProductService)
        self.assertIs(
            product_service.product_repository.connection,
            self.connection,
        )
        self.assertEqual(table, ("products",))
