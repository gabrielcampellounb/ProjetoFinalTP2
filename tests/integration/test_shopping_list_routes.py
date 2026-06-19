import sqlite3
import unittest

from app.web.app import create_app


class TestUS03ShoppingListRoutes(unittest.TestCase):
    """US03: testa a criação HTTP de listas de compras."""

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.app = create_app(self.connection)
        self.client = self.app.test_client()

    def tearDown(self):
        self.connection.close()

    def authenticate_user(self, user_id=7):
        """US03: configura uma sessão de usuário autenticado."""
        with self.client.session_transaction() as flask_session:
            flask_session["user_id"] = user_id
            flask_session["role"] = "user"

    def test_us03_authenticated_user_creates_shopping_list(self):
        """US03: usuário autenticado deve criar lista e receber HTTP 201."""
        self.authenticate_user(user_id=7)

        response = self.client.post(
            "/shopping-lists",
            json={"name": "Compras da semana"},
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsInstance(data["id"], int)
        self.assertEqual(data["user_id"], 7)
        self.assertEqual(data["name"], "Compras da semana")
        self.assertIsInstance(data["created_at"], str)

        stored_user_id = self.connection.execute(
            """
            SELECT user_id
            FROM shopping_lists
            WHERE id = ?;
            """,
            (data["id"],),
        ).fetchone()[0]
        self.assertEqual(stored_user_id, 7)

    def test_us03_reject_empty_name_route(self):
        """US03: nome vazio deve retornar HTTP 400."""
        self.authenticate_user()

        response = self.client.post(
            "/shopping-lists",
            json={"name": " "},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["erro"],
            "O nome da lista de compras não pode estar vazio.",
        )

    def test_us03_reject_unauthenticated_user_route(self):
        """US03: visitante deve receber HTTP 401."""
        response = self.client.post(
            "/shopping-lists",
            json={"name": "Compras da semana"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.get_json()["erro"],
            "Autenticação necessária.",
        )
