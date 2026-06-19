import sqlite3
import unittest

from app.web.app import create_app


class TestAD01ProductRoutes(unittest.TestCase):
    """AD01: testa o cadastro de produtos pela API Flask."""

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.app = create_app(self.conn)
        self.client = self.app.test_client()

    def tearDown(self):
        self.conn.close()

    def test_ad01_create_product_route(self):
        """AD01: produto válido deve retornar HTTP 201 e todos os campos."""
        response = self.client.post(
            "/products",
            json={
                "name": "Arroz",
                "brand": "Tio João",
                "price": 25.90,
                "bar_code": "1234567890123",
                "quantity": 10,
            },
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        self.assertEqual(data["name"], "Arroz")
        self.assertEqual(data["brand"], "Tio João")
        self.assertEqual(data["price"], 25.90)
        self.assertEqual(data["bar_code"], "1234567890123")
        self.assertEqual(data["quantity"], 10)

    def test_ad01_reject_duplicate_bar_code_route(self):
        """AD01: código de barras duplicado deve retornar HTTP 409."""
        payload = {
            "name": "Arroz",
            "brand": "Tio João",
            "price": 25.90,
            "bar_code": "1234567890123",
            "quantity": 10,
        }

        self.client.post("/products", json=payload)
        response = self.client.post("/products", json=payload)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.get_json()["erro"],
            "Já existe um produto com o código de barras 1234567890123.",
        )

    def test_ad01_reject_invalid_product_route(self):
        """AD01: dados inválidos devem retornar HTTP 400."""
        response = self.client.post(
            "/products",
            json={
                "name": "",
                "brand": "Tio João",
                "price": 25.90,
                "bar_code": "1234567890123",
                "quantity": 10,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["erro"],
            "O nome do produto não pode estar vazio.",
        )

    def test_ad01_reject_missing_field_route(self):
        """AD01: campo obrigatório ausente deve retornar HTTP 400."""
        response = self.client.post(
            "/products",
            json={
                "name": "Arroz",
                "brand": "Tio João",
                "price": 25.90,
                "bar_code": "1234567890123",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["erro"],
            "O campo 'quantity' é obrigatório.",
        )
