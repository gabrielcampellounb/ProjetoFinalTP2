"""Persistência SQLite de usuários."""

import sqlite3

from app.domain.exceptions import DuplicateEmailError
from app.domain.user import User


class SQLiteUserRepository:
    """US01: armazena e consulta usuários em SQLite."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """Inicializa o repositório de usuários.

        Pré-condição: connection deve ser uma conexão SQLite aberta.
        Pós-condição: o repositório utiliza a conexão recebida.
        """
        self.connection = connection

    def create_table(self) -> None:
        """US01: cria a tabela de usuários quando necessário.

        Pré-condição: a conexão deve estar aberta.
        Pós-condição: a tabela users existe e a transação é confirmada.
        """
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY COLLATE NOCASE,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
                    CHECK (role IN ('user', 'admin'))
            );
            """
        )
        self.connection.commit()

    def add_user(self, user: User) -> None:
        """US01: persiste um usuário com e-mail único.

        Pré-condição: user deve ser válido e seu e-mail não pode existir.
        Pós-condição: o usuário é salvo ou DuplicateEmailError é lançada.
        """
        if self.get_user_by_email(user.email) is not None:
            raise DuplicateEmailError(
                f"Já existe um usuário com o e-mail {user.email}."
            )

        try:
            cursor = self.connection.execute(
                """
                INSERT INTO users (email, name, password_hash, role)
                VALUES (?, ?, ?, ?);
                """,
                (
                    user.email,
                    user.name,
                    user.password_hash,
                    user.role,
                ),
            )
            self.connection.commit()
            user.user_id = cursor.lastrowid
        except sqlite3.IntegrityError as error:
            raise DuplicateEmailError(
                f"Já existe um usuário com o e-mail {user.email}."
            ) from error

    def get_user_by_email(self, email: str) -> User | None:
        """US01: busca um usuário pelo e-mail.

        Pré-condição: email deve identificar o usuário procurado.
        Pós-condição: retorna o usuário encontrado ou None.
        """
        row = self.connection.execute(
            """
            SELECT rowid, name, email, password_hash, role
            FROM users
            WHERE email = ?;
            """,
            (email,),
        ).fetchone()

        if row is None:
            return None

        return User(
            user_id=row[0],
            name=row[1],
            email=row[2],
            password_hash=row[3],
            role=row[4],
        )
