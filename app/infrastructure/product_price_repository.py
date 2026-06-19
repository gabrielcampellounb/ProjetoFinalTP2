"""Persistência SQLite do histórico de preços observados."""

import sqlite3
from datetime import datetime

from app.domain.product_price import ProductPrice


class SQLiteProductPriceRepository:
    """US06: armazena preços observados sem alterar o preço base."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """US06: inicializa o repositório de preços.

        Pré-condição: connection deve ser uma conexão SQLite aberta.
        Pós-condição: o repositório utiliza a conexão recebida.
        """
        self.connection = connection

    def create_table(self) -> None:
        """US06: cria a tabela independente de histórico de preços.

        Pré-condição: a conexão deve estar aberta.
        Pós-condição: a tabela product_prices existe.
        """
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS product_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_bar_code TEXT NOT NULL,
                store_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                price REAL NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        self.connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_product_prices_product
            ON product_prices (product_bar_code, created_at);
            """
        )
        self.connection.commit()

    def add_price(self, product_price: ProductPrice) -> None:
        """US06: adiciona uma observação ao histórico.

        Pré-condição: product_price deve conter dados validados.
        Pós-condição: um novo registro é persistido sem substituir anteriores.
        """
        self.connection.execute(
            """
            INSERT INTO product_prices (
                product_bar_code,
                store_id,
                user_id,
                price,
                created_at
            )
            VALUES (?, ?, ?, ?, ?);
            """,
            (
                product_price.product_bar_code,
                product_price.store_id,
                product_price.user_id,
                product_price.price,
                product_price.created_at.isoformat(),
            ),
        )
        self.connection.commit()

    def list_prices_by_product(
        self,
        product_bar_code: str,
    ) -> list[ProductPrice]:
        """US06: lista o histórico de um produto.

        Pré-condição: product_bar_code identifica o produto consultado.
        Pós-condição: retorna registros do mais recente para o mais antigo.
        """
        rows = self.connection.execute(
            """
            SELECT product_bar_code, store_id, user_id, price, created_at
            FROM product_prices
            WHERE product_bar_code = ?
            ORDER BY created_at DESC, id DESC;
            """,
            (product_bar_code,),
        ).fetchall()
        return [
            ProductPrice(
                product_bar_code=row[0],
                store_id=row[1],
                user_id=row[2],
                price=row[3],
                created_at=datetime.fromisoformat(row[4]),
            )
            for row in rows
        ]
