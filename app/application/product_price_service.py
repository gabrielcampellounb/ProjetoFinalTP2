"""Casos de uso do histórico de preços por local."""

import math
from datetime import datetime

from app.domain.exceptions import ProductNotFoundError, StoreNotFoundError
from app.domain.product_price import ProductPrice


class ProductPriceService:
    """US06: coordena registro e consulta de preços observados."""

    def __init__(
        self,
        price_repository,
        product_repository,
        store_repository,
    ) -> None:
        """US06: inicializa o serviço de preços observados.

        Pré-condição: os repositórios devem oferecer as operações esperadas.
        Pós-condição: o serviço fica pronto para registrar e consultar preços.
        """
        self.price_repository = price_repository
        self.product_repository = product_repository
        self.store_repository = store_repository

    def register_price(
        self,
        product_bar_code: str,
        store_id: int,
        user_id: int,
        price: int | float,
    ) -> ProductPrice:
        """US06: registra um preço observado por usuário e local.

        Pré-condição: produto e local existem e os dados são válidos.
        Pós-condição: retorna o novo registro persistido.
        """
        product_price = ProductPrice(
            product_bar_code=product_bar_code,
            store_id=store_id,
            user_id=user_id,
            price=price,
            created_at=datetime.now(),
        )
        self._ensure_product_exists(product_bar_code)
        self._ensure_store_exists(store_id)
        self.price_repository.add_price(product_price)
        return product_price

    def list_product_prices(
        self,
        product_bar_code: str,
    ) -> list[ProductPrice]:
        """US06: consulta o histórico de preços de um produto.

        Pré-condição: product_bar_code deve identificar um produto existente.
        Pós-condição: retorna o histórico ordenado pelo repositório.
        """
        self._ensure_product_exists(product_bar_code)
        return self.price_repository.list_prices_by_product(product_bar_code)

    def list_product_price_details(self, product_bar_code: str) -> list[tuple]:
        """US06/WEB: lista preços acompanhados dos locais."""
        return [
            (price, self.store_repository.get_store_by_id(price.store_id))
            for price in self.list_product_prices(product_bar_code)
        ]

    def list_store_products_page(
        self,
        store_id: int,
        query: str,
        page: int,
        page_size: int = 50,
    ) -> tuple[list, int, int, int]:
        """US06/WEB: lista uma página de produtos da loja."""
        self._ensure_store_exists(store_id)
        normalized_query = query.strip()
        total = self.price_repository.count_products_by_store(
            store_id,
            normalized_query,
        )
        total_pages = max(math.ceil(total / page_size), 1)
        current_page = min(max(page, 1), total_pages)
        items = self.price_repository.list_products_by_store(
            store_id=store_id,
            query=normalized_query,
            limit=page_size,
            offset=(current_page - 1) * page_size,
        )
        return items, current_page, total_pages, total

    def _ensure_product_exists(self, product_bar_code: str) -> None:
        """US06: garante que o produto informado esteja cadastrado."""
        if self.product_repository.get_product_by_bar_code(product_bar_code) is None:
            raise ProductNotFoundError(
                f"Produto com o código de barras {product_bar_code} não encontrado."
            )

    def _ensure_store_exists(self, store_id: int) -> None:
        """US06: garante que o local informado esteja cadastrado."""
        if self.store_repository.get_store_by_id(store_id) is None:
            raise StoreNotFoundError(
                f"Local de compra com o identificador {store_id} não encontrado."
            )
