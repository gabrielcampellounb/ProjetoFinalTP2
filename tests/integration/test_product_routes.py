import sqlite3
import unittest

from app.web.app import create_app


class TestProductRoutes(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.app = create_app(self.conn)
        self.client = self.app.test_client()

    def tearDown(self):
        self.conn.close()

    def test_create_product_route(self):
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
        self.assertEqual(data["bar_code"], "1234567890123")

    def test_reject_duplicate_bar_code_route(self):
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

    def test_reject_invalid_product_route(self):
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

    def test_reject_missing_field_route(self):
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
