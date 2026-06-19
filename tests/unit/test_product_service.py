import unittest

from app.application.product_service import ProductService
from app.domain.exceptions import DuplicateBarcodeError, InvalidQuantityError
from app.domain.product import Product


class FakeProductRepository:
    """Simula a persistência de produtos em memória."""

    def __init__(self):
        self.products = {}
        self.last_search_query = None

    def add_product(self, product, quantity):
        self.products[product.bar_code] = (product, quantity)

    def get_product_by_bar_code(self, bar_code):
        return self.products.get(bar_code)

    def search_products_by_text(self, query):
        self.last_search_query = query
        return list(self.products.values())


class TestProductService(unittest.TestCase):
    """Testa os casos de uso de produtos."""

    def setUp(self):
        self.repository = FakeProductRepository()
        self.service = ProductService(self.repository)

        self.product = self.service.create_product(
            name="Produto de teste",
            brand="Marca de teste",
            price=10.0,
            bar_code="1234567890111",
            quantity=5,
        )

    def test_save_valid_product(self):
        """Deve criar e salvar um produto válido."""
        self.assertEqual(self.product.name, "Produto de teste")
        self.assertEqual(self.product.brand, "Marca de teste")
        self.assertEqual(self.product.price, 10.0)
        self.assertEqual(self.product.bar_code, "1234567890111")
        self.assertEqual(len(self.repository.products), 1)
        self.assertEqual(self.repository.products["1234567890111"][1], 5)

    def test_reject_duplicate_bar_code(self):
        """Deve rejeitar um código de barras já cadastrado."""
        with self.assertRaisesRegex(
            DuplicateBarcodeError,
            "^Já existe um produto com o código de barras 1234567890111\\.$",
        ):
            self.service.create_product(
                name="Outro produto",
                brand="Outra marca",
                price=20.0,
                bar_code="1234567890111",
                quantity=5,
            )

        self.assertEqual(len(self.repository.products), 1)

    def test_accept_zero_quantity(self):
        """Deve aceitar quantidade zero como estoque válido."""
        product = self.service.create_product(
            name="Produto sem estoque",
            brand="Marca de teste",
            price=15.0,
            bar_code="1234567890222",
            quantity=0,
        )

        self.assertEqual(self.repository.products[product.bar_code][1], 0)

    def test_reject_negative_quantity(self):
        """Deve rejeitar quantidade negativa sem persistir o produto."""
        with self.assertRaisesRegex(
            InvalidQuantityError,
            "^A quantidade do produto não pode ser negativa\\.$",
        ):
            self.service.create_product(
                name="Produto com estoque inválido",
                brand="Marca de teste",
                price=15.0,
                bar_code="1234567890333",
                quantity=-1,
            )

        self.assertNotIn("1234567890333", self.repository.products)

    def test_reject_non_integer_quantity(self):
        """Deve rejeitar tipos inválidos sem persistir o produto."""
        invalid_quantities = (1.5, "5", True, None, [], object())

        for index, quantity in enumerate(invalid_quantities):
            bar_code = f"1234567{index:06d}"

            with self.subTest(quantity=quantity):
                with self.assertRaisesRegex(
                    InvalidQuantityError,
                    "^A quantidade do produto deve ser um número inteiro\\.$",
                ):
                    self.service.create_product(
                        name="Produto com estoque inválido",
                        brand="Marca de teste",
                        price=15.0,
                        bar_code=bar_code,
                        quantity=quantity,
                    )

                self.assertNotIn(bar_code, self.repository.products)

    def test_us02_search_products_by_text(self):
        """US02: deve buscar produtos usando o texto recebido."""
        expected_product = Product(
            name="Arroz Integral",
            brand="Tio João",
            price=12.50,
            bar_code="1234567890444",
        )
        self.repository.add_product(expected_product, quantity=8)

        results = self.service.search_products("arroz")

        self.assertEqual(self.repository.last_search_query, "arroz")
        self.assertIn((expected_product, 8), results)

    def test_us02_empty_query_returns_empty_list(self):
        """US02: query vazia deve retornar lista vazia sem consultar dados."""
        results = self.service.search_products("   ")

        self.assertEqual(results, [])
        self.assertIsNone(self.repository.last_search_query)
