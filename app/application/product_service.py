from app.domain.product import Product
from app.domain.exceptions import DuplicateBarcodeError

class ProductService:
    def __init__(self, product_repository):
        self.product_repository = product_repository

    def create_product(self, name, brand, price, bar_code, quantity):
        """
        - Creates a new product and saves it to the repository.
        precondition: 
        - name
        - product name, brand, price, bar code, and quantity must be valid.
        - The product must have a unique bar code.
        postcondition:
        - A new product is created and saved in the repository.
        """
        if self.product_repository.get_product_by_bar_code(bar_code):
            raise DuplicateBarcodeError(f"Product with bar code {bar_code} already exists.")

        product = Product(name=name, brand=brand, price=price, bar_code=bar_code)
        self.product_repository.add_product(product, quantity)
        return product