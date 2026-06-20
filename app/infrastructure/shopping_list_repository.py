"""Persistência SQLite de listas de compras."""

import sqlite3
from datetime import datetime

from app.domain.shopping_list import ShoppingList, ShoppingListItem


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
                created_at TEXT NOT NULL,
                favorite INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS shopping_list_items (
                list_id INTEGER NOT NULL,
                bar_code TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                PRIMARY KEY (list_id, bar_code)
            );
            """
        )
        self._ensure_favorite_column()
        self.connection.commit()

    def add_shopping_list(self, shopping_list: ShoppingList) -> None:
        """US03: persiste uma lista de compras.

        Pré-condição: shopping_list deve ser válida e ainda não persistida.
        Pós-condição: a lista recebe id e é salva no banco.
        """
        cursor = self.connection.execute(
            """
            INSERT INTO shopping_lists (user_id, name, created_at, favorite)
            VALUES (?, ?, ?, ?);
            """,
            (
                shopping_list.user_id,
                shopping_list.name,
                shopping_list.created_at.isoformat(),
                int(shopping_list.favorite),
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
            SELECT id, user_id, name, created_at, favorite
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
            favorite=bool(row[4]),
        )

    def list_shopping_lists_by_user(
        self,
        user_id: int,
    ) -> list[ShoppingList]:
        """US03: lista as listas pertencentes a um usuário.

        Pré-condição: user_id identifica o proprietário.
        Pós-condição: retorna as listas ordenadas pela criação.
        """
        rows = self.connection.execute(
            """
            SELECT id, user_id, name, created_at, favorite
            FROM shopping_lists
            WHERE user_id = ?
            ORDER BY id;
            """,
            (user_id,),
        ).fetchall()
        return [
            ShoppingList(
                list_id=row[0],
                user_id=row[1],
                name=row[2],
                created_at=datetime.fromisoformat(row[3]),
                favorite=bool(row[4]),
            )
            for row in rows
        ]

    def set_favorite(self, user_id: int, list_id: int) -> None:
        """US03: mantém uma única lista favorita por usuário.

        Pré-condição: list_id pertence ao user_id informado.
        Pós-condição: somente a lista escolhida fica com favorite igual a um.
        """
        with self.connection:
            self.connection.execute(
                """
                UPDATE shopping_lists
                SET favorite = 0
                WHERE user_id = ?;
                """,
                (user_id,),
            )
            self.connection.execute(
                """
                UPDATE shopping_lists
                SET favorite = 1
                WHERE id = ? AND user_id = ?;
                """,
                (list_id, user_id),
            )

    def add_item(self, item: ShoppingListItem) -> None:
        """US03: persiste um item em uma lista de compras.

        Pré-condição: item deve ser válido e ainda não existir na lista.
        Pós-condição: o item é salvo no banco.
        """
        self.connection.execute(
            """
            INSERT INTO shopping_list_items (list_id, bar_code, quantity)
            VALUES (?, ?, ?);
            """,
            (item.list_id, item.bar_code, item.quantity),
        )
        self.connection.commit()

    def get_item(
        self,
        list_id: int,
        bar_code: str,
    ) -> ShoppingListItem | None:
        """US03: busca um item pelo identificador da lista e produto.

        Pré-condição: list_id e bar_code identificam o item procurado.
        Pós-condição: retorna o item encontrado ou None.
        """
        row = self.connection.execute(
            """
            SELECT list_id, bar_code, quantity
            FROM shopping_list_items
            WHERE list_id = ? AND bar_code = ?;
            """,
            (list_id, bar_code),
        ).fetchone()
        if row is None:
            return None
        return ShoppingListItem(
            list_id=row[0],
            bar_code=row[1],
            quantity=row[2],
        )

    def list_items(self, list_id: int) -> list[ShoppingListItem]:
        """US03: lista todos os itens de uma lista.

        Pré-condição: list_id identifica a lista consultada.
        Pós-condição: retorna os itens ordenados pelo código do produto.
        """
        rows = self.connection.execute(
            """
            SELECT list_id, bar_code, quantity
            FROM shopping_list_items
            WHERE list_id = ?
            ORDER BY bar_code;
            """,
            (list_id,),
        ).fetchall()
        return [
            ShoppingListItem(
                list_id=row[0],
                bar_code=row[1],
                quantity=row[2],
            )
            for row in rows
        ]

    def update_item(self, item: ShoppingListItem) -> None:
        """US03: persiste a nova quantidade de um item.

        Pré-condição: item deve ser válido e existir na lista.
        Pós-condição: a quantidade é atualizada no banco.
        """
        self.connection.execute(
            """
            UPDATE shopping_list_items
            SET quantity = ?
            WHERE list_id = ? AND bar_code = ?;
            """,
            (item.quantity, item.list_id, item.bar_code),
        )
        self.connection.commit()

    def remove_item(self, list_id: int, bar_code: str) -> None:
        """US03: remove um item da lista.

        Pré-condição: list_id e bar_code identificam um item existente.
        Pós-condição: o item é removido do banco.
        """
        self.connection.execute(
            """
            DELETE FROM shopping_list_items
            WHERE list_id = ? AND bar_code = ?;
            """,
            (list_id, bar_code),
        )
        self.connection.commit()

    def _ensure_favorite_column(self) -> None:
        """US03: adiciona favorite a bancos criados anteriormente."""
        columns = self.connection.execute(
            "PRAGMA table_info(shopping_lists);"
        ).fetchall()
        if "favorite" not in {column[1] for column in columns}:
            self.connection.execute(
                """
                ALTER TABLE shopping_lists
                ADD COLUMN favorite INTEGER NOT NULL DEFAULT 0;
                """
            )
