import sqlite3
import unittest

from app.web.app import create_app


class TestUS06ProductPriceRoutes(unittest.TestCase):
    """US06: testa registro e consulta HTTP de preços por local."""

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.app = create_app(self.connection)
        self.client = self.app.test_client()
        self._create_product_and_store()

    def tearDown(self):
        self.connection.close()

    def authenticate_as(self, role="user", user_id=7):
        """US06: configura uma sessão autenticada para o teste."""
        with self.client.session_transaction() as flask_session:
            flask_session.clear()
            flask_session["user_id"] = user_id
            flask_session["role"] = role

    def clear_session(self):
        """US06: remove a autenticação da sessão de teste."""
        with self.client.session_transaction() as flask_session:
            flask_session.clear()

    def _create_product_and_store(self):
        """US06: prepara produto e local existentes para os testes."""
        self.authenticate_as(role="admin", user_id=1)
        self.client.post(
            "/products",
            json={
                "name": "Arroz",
                "brand": "Marca A",
                "price": 10.0,
                "bar_code": "1234567890123",
                "quantity": 5,
            },
        )
        response = self.client.post(
            "/stores",
            json={
                "name": "Mercado Central",
                "address": "Rua Principal, 100",
            },
        )
        self.store_id = response.get_json()["id"]
        self.authenticate_as()

    def test_us06_authenticated_user_registers_product_price(self):
        """US06: usuário autenticado deve registrar preço e receber HTTP 201."""
        response = self.client.post(
            "/prices",
            json={
                "product_bar_code": "1234567890123",
                "store_id": self.store_id,
                "price": 8.75,
            },
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["product_bar_code"], "1234567890123")
        self.assertEqual(data["store_id"], self.store_id)
        self.assertEqual(data["user_id"], 7)
        self.assertEqual(data["price"], 8.75)
        self.assertIsInstance(data["created_at"], str)

    def test_us06_reject_price_for_missing_product_route(self):
        """US06: produto inexistente deve retornar HTTP 404."""
        response = self.client.post(
            "/prices",
            json={
                "product_bar_code": "9999999999999",
                "store_id": self.store_id,
                "price": 8.75,
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_us06_reject_price_for_missing_store_route(self):
        """US06: local inexistente deve retornar HTTP 404."""
        response = self.client.post(
            "/prices",
            json={
                "product_bar_code": "1234567890123",
                "store_id": 999,
                "price": 8.75,
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_us06_reject_negative_price_route(self):
        """US06: preço negativo deve retornar HTTP 400."""
        response = self.client.post(
            "/prices",
            json={
                "product_bar_code": "1234567890123",
                "store_id": self.store_id,
                "price": -0.01,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_us06_list_product_prices_route(self):
        """US06: consulta deve retornar preços do produto por local."""
        self.client.post(
            "/prices",
            json={
                "product_bar_code": "1234567890123",
                "store_id": self.store_id,
                "price": 8.75,
            },
        )

        response = self.client.get("/products/1234567890123/prices")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(response.get_json()[0]["store_id"], self.store_id)
        self.assertEqual(response.get_json()[0]["price"], 8.75)

    def test_us06_reject_unauthenticated_price_routes(self):
        """US06: visitante não deve registrar nem consultar preços."""
        self.clear_session()

        post_response = self.client.post(
            "/prices",
            json={
                "product_bar_code": "1234567890123",
                "store_id": self.store_id,
                "price": 8.75,
            },
        )
        get_response = self.client.get("/products/1234567890123/prices")

        self.assertEqual(post_response.status_code, 401)
        self.assertEqual(get_response.status_code, 401)
