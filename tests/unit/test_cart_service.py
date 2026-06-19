import unittest
from types import SimpleNamespace

from app.application.cart_service import CartService
from app.domain.exceptions import InvalidCartError


class TestUS05CartService(unittest.TestCase):
    """US05: testa o cálculo puro do total estimado do carrinho."""

    def test_us05_empty_cart_total_is_zero(self):
        """US05: carrinho vazio deve possuir total estimado zero."""
        total = CartService.calculate_total([])

        self.assertEqual(total, 0)

    def test_us05_single_item_total(self):
        """US05: um item deve retornar preço multiplicado pela quantidade."""
        product = SimpleNamespace(price=12.50)

        total = CartService.calculate_total([(product, 2)])

        self.assertEqual(total, 25.0)

    def test_us05_multiple_items_total(self):
        """US05: vários itens devem retornar a soma dos subtotais."""
        rice = SimpleNamespace(price=12.50)
        beans = SimpleNamespace(price=8.90)

        total = CartService.calculate_total(
            [
                (rice, 2),
                (beans, 3),
            ]
        )

        self.assertAlmostEqual(total, 51.70)

    def test_us05_reject_invalid_product_price(self):
        """US05: preço inválido deve gerar erro controlado."""
        invalid_product = SimpleNamespace(price="12.50")

        with self.assertRaisesRegex(
            InvalidCartError,
            "^O preço do item do carrinho é inválido\\.$",
        ):
            CartService.calculate_total([(invalid_product, 2)])
