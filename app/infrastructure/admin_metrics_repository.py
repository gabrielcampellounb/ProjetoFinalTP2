"""Consultas SQLite para métricas administrativas."""

import sqlite3


class SQLiteAdminMetricsRepository:
    """AD04: consulta contagens simples das tabelas da aplicação."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """AD04: inicializa o repositório de métricas.

        Pré-condição: connection deve ser uma conexão SQLite aberta.
        Pós-condição: o repositório utiliza a conexão recebida.
        """
        self.connection = connection

    def get_metrics(self) -> dict[str, int]:
        """AD04: retorna as contagens administrativas.

        Pré-condição: as tabelas da aplicação devem existir.
        Pós-condição: retorna quatro totais inteiros obtidos do SQLite.
        """
        row = self.connection.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM products),
                (SELECT COUNT(*) FROM users),
                (SELECT COUNT(*) FROM shopping_lists),
                (SELECT COUNT(*) FROM product_prices);
            """
        ).fetchone()
        return {
            "total_products": row[0],
            "total_users": row[1],
            "total_shopping_lists": row[2],
            "total_registered_prices": row[3],
        }
