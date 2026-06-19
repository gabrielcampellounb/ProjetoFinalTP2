"""Casos de uso relacionados a produtos."""

from app.domain.exceptions import DuplicateBarcodeError
from app.domain.product import Product


class ProductService:
    """Coordena regras de aplicação e persistência de produtos."""

    def __init__(self, product_repository) -> None:
        """Inicializa o serviço.

        Pré: product_repository deve implementar busca e inclusão.
        Pós: o serviço fica pronto para executar seus casos de uso.
        """
        self.product_repository = product_repository

    def create_product(
        self,
        name: str,
        brand: str,
        price: int | float,
        bar_code: str,
        quantity: int,
    ) -> Product:
        """Cria e persiste um produto.

        Pré: os dados devem ser válidos e o código deve ser único.
        Pós: retorna o produto salvo ou lança DuplicateBarcodeError.
        """
        stored_product = self.product_repository.get_product_by_bar_code(bar_code)
        if stored_product is not None:
            raise DuplicateBarcodeError(
                f"Product with bar code {bar_code} already exists."
            )

        product = Product(
            name=name,
            brand=brand,
            price=price,
            bar_code=bar_code,
        )
        self.product_repository.add_product(product, quantity)
        return product
