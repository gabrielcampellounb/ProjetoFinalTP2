"""Persistência SQLite de produtos."""

import sqlite3

from app.domain.exceptions import DuplicateBarcodeError
from app.domain.product import Product
from app.domain.quantity import validate_quantity


class SQLiteProductRepository:
    """Armazena e consulta produtos em uma conexão SQLite."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """Inicializa o repositório.

        Pré-condição: connection deve ser uma conexão SQLite aberta.
        Pós-condição: o repositório passa a utilizar a conexão recebida.
        """
        self.connection = connection

    def create_table(self) -> None:
        """Cria a tabela de produtos quando necessário.

        Pré-condição: a conexão deve estar aberta.
        Pós-condição: a tabela existe e a transação é confirmada.
        """
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                bar_code TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                brand TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            );
            """
        )
        self.connection.commit()

    def add_product(self, product: Product, quantity: int) -> None:
        """Persiste um produto e sua quantidade.

        Pré-condição: produto e quantidade válidos, com código ainda livre.
        Pós-condição: o registro é salvo ou uma exceção é lançada.
        """
        validate_quantity(quantity)

        if self.get_product_by_bar_code(product.bar_code) is not None:
            raise DuplicateBarcodeError(
                "Já existe um produto com o código de barras "
                f"{product.bar_code}."
            )

        self.connection.execute(
            """
            INSERT INTO products (bar_code, name, brand, price, quantity)
            VALUES (?, ?, ?, ?, ?);
            """,
            (
                product.bar_code,
                product.name,
                product.brand,
                product.price,
                quantity,
            ),
        )
        self.connection.commit()

    def get_product_by_bar_code(
        self,
        bar_code: str,
    ) -> tuple[Product, int] | None:
        """Busca um produto pelo código de barras.

        Pré-condição: bar_code deve identificar o registro procurado.
        Pós-condição: retorna produto e quantidade, ou None quando ausente.
        """
        row = self.connection.execute(
            """
            SELECT bar_code, name, brand, price, quantity
            FROM products
            WHERE bar_code = ?;
            """,
            (bar_code,),
        ).fetchone()

        if row is None:
            return None

        return self._to_product_with_quantity(row)

    def search_products_by_text(
        self,
        query: str,
    ) -> list[tuple[Product, int]]:
        """US02: busca produtos por parte do nome ou da marca.

        Pré-condição: query deve conter um texto não vazio.
        Pós-condição: retorna produtos compatíveis ou lista vazia.
        """
        search_pattern = f"%{query}%"
        rows = self.connection.execute(
            """
            SELECT bar_code, name, brand, price, quantity
            FROM products
            WHERE name LIKE ? COLLATE NOCASE
               OR brand LIKE ? COLLATE NOCASE
            ORDER BY name, bar_code;
            """,
            (search_pattern, search_pattern),
        ).fetchall()

        return [self._to_product_with_quantity(row) for row in rows]

    @staticmethod
    def _to_product_with_quantity(row) -> tuple[Product, int]:
        """US02: converte uma linha SQLite em produto e quantidade."""
        product = Product(
            name=row[1],
            brand=row[2],
            price=row[3],
            bar_code=row[0],
        )
        return product, row[4]
