import unittest

from app.domain.product import Product
from app.domain.exceptions import InvalidProductError

class TestProductCreation(unittest.TestCase):
    def test_create_product(self):
        """Product should be created with valid attributes."""
        product = Product(
            name="Test product",
            brand="Test brand",
            price=10.0,
            bar_code="1234567890123"
            )
        self.assertEqual(product.name, "Test product")
        self.assertEqual(product.brand, "Test brand")
        self.assertEqual(product.price, 10.0)
        self.assertEqual(product.bar_code, "1234567890123")

    def test_create_product_invalid_price(self):
        """Creating a product with a negative price 
           should raise an InvalidProductError."""
        with self.assertRaises(InvalidProductError):
            Product(
                name="Test product",
                brand="Test brand",
                price=-10.0,
                bar_code="1234567890123"
            )
            self.assertRaises(InvalidProductError)
    
    def test_create_product_invalid_bar_code(self):
        """Creating a product with an invalid bar code 
           should raise an InvalidProductError."""
        with self.assertRaises(InvalidProductError):
            Product(
                name="Test product",
                brand="Test brand",
                price=10.0,
                bar_code="invalid_bar_code"
            )
            self.assertRaises(InvalidProductError)
    
    def test_create_product_empty_name(self):
        """Creating a product with an empty name 
           should raise an InvalidProductError."""
        with self.assertRaises(InvalidProductError):
            Product(
                name="",
                brand="Test brand",
                price=10.0,
                bar_code="1234567890123"
            )
            self.assertRaises(InvalidProductError)

    def test_create_product_empty_brand(self):
        """Creating a product with an empty brand 
           should raise an InvalidProductError."""
        with self.assertRaises(InvalidProductError):
            Product(
                name="Test product",
                brand="",
                price=10.0,
                bar_code="1234567890123"
            )
            self.assertRaises(InvalidProductError)

class TestProductUpdate(unittest.TestCase):
    def setUp(self):
        self.product = Product(
            name="Test product",
            brand="Test brand",
            price=10.0,
            bar_code="1234567890123"
        )

    def test_update_product_price(self):
        """Updating the product price should work correctly."""
        self.product.price = 20.0
        self.assertEqual(self.product.price, 20.0)

    def test_update_product_invalid_price(self):
        """Updating the product price to a negative value 
           should raise an InvalidProductError."""
        with self.assertRaises(InvalidProductError):
            self.product.price = -5.0
            self.assertRaises(InvalidProductError)

    def test_update_product_invalid_bar_code(self):
        """Updating the product bar code to an invalid value 
           should raise an InvalidProductError."""
        with self.assertRaises(InvalidProductError):
            self.product.bar_code = "invalid_bar_code"
            self.assertRaises(InvalidProductError)
        with self.assertRaises(InvalidProductError):
            self.product.bar_code = "123456789012"  # 12 digits instead of 13
            self.assertRaises(InvalidProductError)
    
    def test_update_product_empty_name(self):
        """Updating the product name to an empty value 
           should raise an InvalidProductError."""
        with self.assertRaises(InvalidProductError):
            self.product.name = ""
            self.assertRaises(InvalidProductError)

    def test_update_product_empty_brand(self):
        """Updating the product brand to an empty value 
           should raise an InvalidProductError."""
        with self.assertRaises(InvalidProductError):
            self.product.brand = ""
            self.assertRaises(InvalidProductError)

    def test_access_product_attributes(self):
        """Accessing product attributes should return the correct values."""
        self.assertEqual(self.product.name, "Test product")
        self.assertEqual(self.product.brand, "Test brand")
        self.assertEqual(self.product.price, 10.0)
        self.assertEqual(self.product.bar_code, "1234567890123")

        