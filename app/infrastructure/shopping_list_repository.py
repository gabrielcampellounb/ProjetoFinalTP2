"""Persistência SQLite de listas de compras."""

import sqlite3
from datetime import datetime

from app.domain.shopping_list import ShoppingList


class SQLiteShoppingListRepository:
    """US03: armazena e consulta listas de compras em SQLite."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """Inicializa o repositório de listas.

        Pré-condição: connection deve ser uma conexão SQLite aberta.
        Pós-condição: o repositório utiliza a conexão recebida.
        """
        self.connection = connection

    def create_table(self) -> None:
        """US03: cria a tabela de listas quando necessário.

        Pré-condição: a conexão deve estar aberta.
        Pós-condição: a tabela shopping_lists existe.
        """
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS shopping_lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        self.connection.commit()

    def add_shopping_list(self, shopping_list: ShoppingList) -> None:
        """US03: persiste uma lista de compras.

        Pré-condição: shopping_list deve ser válida e ainda não persistida.
        Pós-condição: a lista recebe id e é salva no banco.
        """
        cursor = self.connection.execute(
            """
            INSERT INTO shopping_lists (user_id, name, created_at)
            VALUES (?, ?, ?);
            """,
            (
                shopping_list.user_id,
                shopping_list.name,
                shopping_list.created_at.isoformat(),
            ),
        )
        self.connection.commit()
        shopping_list.list_id = cursor.lastrowid

    def get_shopping_list_by_id(
        self,
        list_id: int,
    ) -> ShoppingList | None:
        """US03: busca uma lista pelo identificador.

        Pré-condição: list_id deve identificar a lista procurada.
        Pós-condição: retorna a lista encontrada ou None.
        """
        row = self.connection.execute(
            """
            SELECT id, user_id, name, created_at
            FROM shopping_lists
            WHERE id = ?;
            """,
            (list_id,),
        ).fetchone()

        if row is None:
            return None

        return ShoppingList(
            list_id=row[0],
            user_id=row[1],
            name=row[2],
            created_at=datetime.fromisoformat(row[3]),
        )
