import unittest

from app.application.product_service import ProductService
from app.domain.exceptions import DuplicateBarcodeError

class FakeProductRepository:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_product_by_bar_code(self, bar_code):
        for product in self.products:
            if product.bar_code == bar_code:
                return product
        return None

class TestProductService(unittest.TestCase):
    def setUp(self):
        self.repository = FakeProductRepository()
        self.service = ProductService(self.repository)

        self.product = self.service.create_product(
            name="Test Product", 
            brand="Test Brand",
            price=10.0,
            bar_code="1234567890"
        )

    def test_if_product_is_saved(self):
        """
        Ensure the product is valid 
        and is saved in the repository.
        """
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.brand, "Test Brand")
        self.assertEqual(self.product.price, 10.0)
        self.assertEqual(self.product.bar_code, "1234567890")

        self.assertEqual(len(self.repository.products), 1)

    def test_reject_duplicate_bar_code(self):
        """Ensure that creating a product 
        with a duplicate bar code raises an error."""
        with self.assertRaises(DuplicateBarcodeError):
            self.service.create_product(
                name="Another Product", 
                brand="Another Brand",
                price=20.0,
                bar_code="1234567890"
            )

    
        