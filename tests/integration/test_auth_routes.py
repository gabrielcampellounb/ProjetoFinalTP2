import sqlite3
import unittest

from app.web.app import create_app


class TestUS01AuthRoutes(unittest.TestCase):
    """US01: testa cadastro, login e logout com sessão Flask."""

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.app = create_app(self.connection)
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self):
        self.connection.close()

    def register_user(self):
        """US01: cadastra um usuário válido para os testes de autenticação."""
        return self.client.post(
            "/auth/register",
            json={
                "name": "Maria Silva",
                "email": "maria@example.com",
                "password": "senha-segura",
            },
        )

    def test_us01_register_user_route(self):
        """US01: cadastro válido deve retornar HTTP 201 sem expor hash."""
        response = self.register_user()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {
                "name": "Maria Silva",
                "email": "maria@example.com",
                "role": "user",
            },
        )
        stored_password = self.connection.execute(
            """
            SELECT password_hash
            FROM users
            WHERE email = ?;
            """,
            ("maria@example.com",),
        ).fetchone()[0]
        self.assertNotEqual(stored_password, "senha-segura")

    def test_us01_login_valid_user_stores_session(self):
        """US01: login válido deve retornar 200 e gravar usuário e papel."""
        self.register_user()

        response = self.client.post(
            "/auth/login",
            json={
                "email": "maria@example.com",
                "password": "senha-segura",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["role"], "user")
        with self.client.session_transaction() as flask_session:
            self.assertIsInstance(flask_session["user_id"], int)
            self.assertEqual(flask_session["role"], "user")

    def test_us01_reject_invalid_login(self):
        """US01: credenciais inválidas devem retornar HTTP 401 sem sessão."""
        self.register_user()

        response = self.client.post(
            "/auth/login",
            json={
                "email": "maria@example.com",
                "password": "senha-incorreta",
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.get_json()["erro"],
            "E-mail ou senha inválidos.",
        )
        with self.client.session_transaction() as flask_session:
            self.assertNotIn("user_id", flask_session)
            self.assertNotIn("role", flask_session)

    def test_us01_logout_clears_session(self):
        """US01: logout deve limpar a sessão e retornar HTTP 204."""
        self.register_user()
        self.client.post(
            "/auth/login",
            json={
                "email": "maria@example.com",
                "password": "senha-segura",
            },
        )

        response = self.client.post("/auth/logout")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")
        with self.client.session_transaction() as flask_session:
            self.assertNotIn("user_id", flask_session)
            self.assertNotIn("role", flask_session)
