import sqlite3
import unittest

from app.web.app import create_app


class TestProductRoutes(unittest.TestCase):
    """Testa AD01, US02, AD02, AD03 e autorização RNF02."""

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.app = create_app(self.conn)
        self.client = self.app.test_client()
        self.authenticate_as("admin")

    def tearDown(self):
        self.conn.close()

    def authenticate_as(self, role):
        """RNF02: configura uma sessão autenticada para os testes."""
        with self.client.session_transaction() as flask_session:
            flask_session.clear()
            flask_session["user_id"] = 1
            flask_session["role"] = role

    def clear_session(self):
        """RNF02: remove a autenticação da sessão de teste."""
        with self.client.session_transaction() as flask_session:
            flask_session.clear()

    @staticmethod
    def protected_requests():
        """RNF02: retorna exemplos das quatro operações administrativas."""
        return (
            (
                "POST",
                "/products",
                {
                    "name": "Arroz",
                    "brand": "Tio João",
                    "price": 25.90,
                    "bar_code": "1234567890123",
                    "quantity": 10,
                },
            ),
            (
                "PUT",
                "/products/1234567890123",
                {
                    "name": "Arroz Integral",
                    "brand": "Tio João",
                    "price": 30.50,
                },
            ),
            ("DELETE", "/products/1234567890123", None),
            (
                "PATCH",
                "/products/1234567890123/stock",
                {"quantity": 20},
            ),
        )

    def test_ad01_create_product_route(self):
        """AD01/RNF02: admin deve cadastrar produto e receber HTTP 201."""
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
        """AD01/RNF02: admin recebe 409 para código de barras duplicado."""
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
        """AD01/RNF02: dados inválidos do admin devem retornar HTTP 400."""
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
        """AD01/RNF02: campo ausente do admin deve retornar HTTP 400."""
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

    def test_us02_search_products_route(self):
        """US02/RNF02: GET público deve buscar por parte do nome."""
        self.client.post(
            "/products",
            json={
                "name": "Arroz Integral",
                "brand": "Tio João",
                "price": 12.50,
                "bar_code": "1234567890444",
                "quantity": 8,
            },
        )
        self.client.post(
            "/products",
            json={
                "name": "Feijão Carioca",
                "brand": "Camil",
                "price": 8.90,
                "bar_code": "1234567890555",
                "quantity": 5,
            },
        )

        response = self.client.get("/products?q=arroz")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            [
                {
                    "name": "Arroz Integral",
                    "brand": "Tio João",
                    "price": 12.50,
                    "bar_code": "1234567890444",
                    "quantity": 8,
                }
            ],
        )

    def test_us02_search_products_by_brand_route(self):
        """US02/RNF02: GET público deve buscar por parte da marca."""
        self.client.post(
            "/products",
            json={
                "name": "Feijão Carioca",
                "brand": "Camil Alimentos",
                "price": 8.90,
                "bar_code": "1234567890555",
                "quantity": 5,
            },
        )

        response = self.client.get("/products?q=camil")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["brand"], "Camil Alimentos")

    def test_us02_search_without_results_returns_empty_list(self):
        """US02/RNF02: busca pública sem resultado retorna lista vazia."""
        response = self.client.get("/products?q=inexistente")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_us02_empty_query_returns_empty_list(self):
        """US02/RNF02: query pública vazia deve retornar lista vazia."""
        response = self.client.get("/products?q=")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_ad02_update_existing_product_route(self):
        """AD02/RNF02: admin deve editar produto e receber HTTP 200."""
        self.client.post(
            "/products",
            json={
                "name": "Arroz",
                "brand": "Tio João",
                "price": 25.90,
                "bar_code": "1234567890123",
                "quantity": 10,
            },
        )

        response = self.client.put(
            "/products/1234567890123",
            json={
                "name": "Arroz Integral",
                "brand": "Nova Marca",
                "price": 30.50,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "name": "Arroz Integral",
                "brand": "Nova Marca",
                "price": 30.50,
                "bar_code": "1234567890123",
                "quantity": 10,
            },
        )

    def test_ad02_update_missing_product_route(self):
        """AD02/RNF02: admin recebe 404 ao editar produto inexistente."""
        response = self.client.put(
            "/products/9999999999999",
            json={
                "name": "Produto atualizado",
                "brand": "Marca atualizada",
                "price": 30.50,
            },
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["erro"],
            "Produto com o código de barras 9999999999999 não encontrado.",
        )

    def test_ad02_reject_invalid_update_route(self):
        """AD02/RNF02: edição inválida do admin deve retornar HTTP 400."""
        self.client.post(
            "/products",
            json={
                "name": "Arroz",
                "brand": "Tio João",
                "price": 25.90,
                "bar_code": "1234567890123",
                "quantity": 10,
            },
        )

        response = self.client.put(
            "/products/1234567890123",
            json={
                "name": "",
                "brand": "Nova Marca",
                "price": 30.50,
            },
        )

        self.assertEqual(response.status_code, 400)

        stored_product = self.conn.execute(
            """
            SELECT name, brand, price
            FROM products
            WHERE bar_code = ?;
            """,
            ("1234567890123",),
        ).fetchone()
        self.assertEqual(stored_product, ("Arroz", "Tio João", 25.90))

    def test_ad02_deactivate_existing_product_route(self):
        """AD02/RNF02: admin deve desativar produto e receber HTTP 204."""
        self.client.post(
            "/products",
            json={
                "name": "Arroz Integral",
                "brand": "Tio João",
                "price": 12.50,
                "bar_code": "1234567890444",
                "quantity": 8,
            },
        )

        response = self.client.delete("/products/1234567890444")
        search_response = self.client.get("/products?q=arroz")
        stored_row = self.conn.execute(
            """
            SELECT active
            FROM products
            WHERE bar_code = ?;
            """,
            ("1234567890444",),
        ).fetchone()

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")
        self.assertEqual(search_response.status_code, 200)
        self.assertEqual(search_response.get_json(), [])
        self.assertEqual(stored_row, (0,))

    def test_ad02_deactivate_missing_product_route(self):
        """AD02/RNF02: admin recebe 404 ao remover produto inexistente."""
        response = self.client.delete("/products/9999999999999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["erro"],
            "Produto com o código de barras 9999999999999 não encontrado.",
        )

    def test_ad03_update_existing_product_stock_route(self):
        """AD03/RNF02: admin deve atualizar estoque e receber HTTP 200."""
        self.client.post(
            "/products",
            json={
                "name": "Arroz Integral",
                "brand": "Tio João",
                "price": 12.50,
                "bar_code": "1234567890444",
                "quantity": 8,
            },
        )

        response = self.client.patch(
            "/products/1234567890444/stock",
            json={"quantity": 20},
        )
        search_response = self.client.get("/products?q=arroz")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["quantity"], 20)
        self.assertEqual(search_response.get_json()[0]["quantity"], 20)

    def test_ad03_reject_negative_stock_route(self):
        """AD03/RNF02: estoque inválido do admin deve retornar HTTP 400."""
        self.client.post(
            "/products",
            json={
                "name": "Arroz Integral",
                "brand": "Tio João",
                "price": 12.50,
                "bar_code": "1234567890444",
                "quantity": 8,
            },
        )

        response = self.client.patch(
            "/products/1234567890444/stock",
            json={"quantity": -1},
        )
        stored_quantity = self.conn.execute(
            """
            SELECT quantity
            FROM products
            WHERE bar_code = ?;
            """,
            ("1234567890444",),
        ).fetchone()[0]

        self.assertEqual(response.status_code, 400)
        self.assertEqual(stored_quantity, 8)

    def test_ad03_reject_stock_update_for_missing_product_route(self):
        """AD03/RNF02: admin recebe 404 para estoque de produto ausente."""
        response = self.client.patch(
            "/products/9999999999999/stock",
            json={"quantity": 20},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["erro"],
            "Produto com o código de barras 9999999999999 não encontrado.",
        )

    def test_rnf02_reject_unauthenticated_admin_routes(self):
        """AD01/AD02/AD03/RNF02: visitante recebe 401 nas rotas admin."""
        self.clear_session()

        for method, path, payload in self.protected_requests():
            with self.subTest(method=method, path=path):
                response = self.client.open(
                    path,
                    method=method,
                    json=payload,
                )

                self.assertEqual(response.status_code, 401)
                self.assertEqual(
                    response.get_json()["erro"],
                    "Autenticação necessária.",
                )

    def test_rnf02_reject_common_user_on_admin_routes(self):
        """AD01/AD02/AD03/RNF02: usuário comum recebe 403 nas rotas admin."""
        self.authenticate_as("user")

        for method, path, payload in self.protected_requests():
            with self.subTest(method=method, path=path):
                response = self.client.open(
                    path,
                    method=method,
                    json=payload,
                )

                self.assertEqual(response.status_code, 403)
                self.assertEqual(
                    response.get_json()["erro"],
                    "Acesso permitido apenas para administradores.",
                )

    def test_us02_rnf02_product_search_remains_public(self):
        """US02/RNF02: visitante deve continuar acessando GET /products."""
        self.client.post(
            "/products",
            json={
                "name": "Arroz Integral",
                "brand": "Tio João",
                "price": 12.50,
                "bar_code": "1234567890444",
                "quantity": 8,
            },
        )
        self.clear_session()

        response = self.client.get("/products?q=arroz")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["name"], "Arroz Integral")
