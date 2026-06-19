import unittest

from app.application.product_service import ProductService
from app.domain.exceptions import DuplicateBarcodeError

class FakeProductRepository:
    def __init__(self):
        self.products = dict() 

    def add_product(self, product, quantity):
        self.products[product.bar_code] = (product, quantity)

    def get_product_by_bar_code(self, bar_code):
        return self.products.get(bar_code)

class TestProductService(unittest.TestCase):
    def setUp(self):
        self.repository = FakeProductRepository()
        self.service = ProductService(self.repository)

        self.product = self.service.create_product(
            name="Test Product", 
            brand="Test Brand",
            price=10.0,
            bar_code="1234567890111",
            quantity=5
        )

    def test_if_product_is_saved(self):
        """
        Ensure the product is valid 
        and is saved in the repository.
        """
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.brand, "Test Brand")
        self.assertEqual(self.product.price, 10.0)
        self.assertEqual(self.product.bar_code, "1234567890111")

        self.assertEqual(len(self.repository.products), 1)
        self.assertEqual(self.repository.products["1234567890111"][1], 5)

    def test_reject_duplicate_bar_code(self):
        """Ensure that creating a product 
        with a duplicate bar code raises an error."""
        with self.assertRaises(DuplicateBarcodeError):
            self.service.create_product(
                name="Another Product", 
                brand="Another Brand",
                price=20.0,
                bar_code="1234567890111",
                quantity=5
            )
