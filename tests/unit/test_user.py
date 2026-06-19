import unittest

from app.domain.exceptions import InvalidUserError
from app.domain.user import User


class TestUS01User(unittest.TestCase):
    """US01: testa as regras da entidade de usuário."""

    def test_us01_create_valid_user(self):
        """US01: deve criar usuário com dados e papel válidos."""
        user = User(
            name="Maria Silva",
            email="maria@example.com",
            password_hash="hash-seguro",
            role="user",
        )

        self.assertEqual(user.name, "Maria Silva")
        self.assertEqual(user.email, "maria@example.com")
        self.assertEqual(user.password_hash, "hash-seguro")
        self.assertEqual(user.role, "user")

    def test_us01_normalize_email(self):
        """US01: deve normalizar o e-mail para minúsculas."""
        user = User(
            name="Maria Silva",
            email="MARIA@EXAMPLE.COM",
            password_hash="hash-seguro",
            role="user",
        )

        self.assertEqual(user.email, "maria@example.com")

    def test_us01_reject_empty_or_invalid_email(self):
        """US01: deve rejeitar e-mail vazio ou inválido."""
        invalid_emails = ("", "   ", "maria", "@example.com", "maria@")

        for email in invalid_emails:
            with self.subTest(email=email):
                with self.assertRaises(InvalidUserError):
                    User(
                        name="Maria Silva",
                        email=email,
                        password_hash="hash-seguro",
                        role="user",
                    )

    def test_us01_reject_invalid_role(self):
        """US01: deve aceitar somente os papéis user e admin."""
        with self.assertRaisesRegex(
            InvalidUserError,
            "^O papel do usuário deve ser 'user' ou 'admin'\\.$",
        ):
            User(
                name="Maria Silva",
                email="maria@example.com",
                password_hash="hash-seguro",
                role="manager",
            )
