"""Persistência SQLite de locais de compra."""

import sqlite3

from app.domain.store import Store


class SQLiteStoreRepository:
    """US06: armazena e consulta locais de compra em SQLite."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """Inicializa o repositório de locais.

        Pré-condição: connection deve ser uma conexão SQLite aberta.
        Pós-condição: o repositório utiliza a conexão recebida.
        """
        self.connection = connection

    def create_table(self) -> None:
        """US06: cria a tabela de locais quando necessário.

        Pré-condição: a conexão deve estar aberta.
        Pós-condição: a tabela stores existe.
        """
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS stores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                observation TEXT,
                latitude REAL,
                longitude REAL
            );
            """
        )
        self._ensure_coordinate_columns()
        self.connection.commit()

    def add_store(self, store: Store) -> None:
        """US06: persiste um local de compra.

        Pré-condição: store deve ser válido e ainda não persistido.
        Pós-condição: o local recebe id e é salvo no banco.
        """
        cursor = self.connection.execute(
            """
            INSERT INTO stores (name, address, observation, latitude, longitude)
            VALUES (?, ?, ?, ?, ?);
            """,
            (
                store.name,
                store.address,
                store.observation,
                store.latitude,
                store.longitude,
            ),
        )
        self.connection.commit()
        store.store_id = cursor.lastrowid

    def list_stores(self) -> list[Store]:
        """US06: lista os locais cadastrados.

        Pré-condição: a tabela stores deve existir.
        Pós-condição: retorna os locais ordenados por nome e id.
        """
        rows = self.connection.execute(
            """
            SELECT id, name, address, observation, latitude, longitude
            FROM stores
            ORDER BY name COLLATE NOCASE, id;
            """
        ).fetchall()
        return [
            Store(
                store_id=row[0],
                name=row[1],
                address=row[2],
                observation=row[3],
                latitude=row[4],
                longitude=row[5],
            )
            for row in rows
        ]

    def get_store_by_id(self, store_id: int) -> Store | None:
        """US06: busca um local pelo identificador.

        Pré-condição: store_id deve identificar o local procurado.
        Pós-condição: retorna o local encontrado ou None.
        """
        row = self.connection.execute(
            """
            SELECT id, name, address, observation, latitude, longitude
            FROM stores
            WHERE id = ?;
            """,
            (store_id,),
        ).fetchone()
        if row is None:
            return None
        return Store(
            store_id=row[0],
            name=row[1],
            address=row[2],
            observation=row[3],
            latitude=row[4],
            longitude=row[5],
        )

    def update_store_coordinates(
        self,
        store_id: int,
        latitude: float,
        longitude: float,
    ) -> None:
        """US06/GPS: atualiza as coordenadas de um local existente.

        Pré-condição: store_id deve existir e coordenadas devem ser válidas.
        Pós-condição: latitude e longitude ficam persistidas no SQLite.
        """
        self.connection.execute(
            """
            UPDATE stores
            SET latitude = ?, longitude = ?
            WHERE id = ?;
            """,
            (latitude, longitude, store_id),
        )
        self.connection.commit()

    def _ensure_coordinate_columns(self) -> None:
        """US06/GPS: migra bancos antigos com colunas de coordenadas.

        Pré-condição: a tabela stores deve existir.
        Pós-condição: latitude e longitude existem na tabela.
        """
        columns = {
            row[1]
            for row in self.connection.execute("PRAGMA table_info(stores);").fetchall()
        }
        if "latitude" not in columns:
            self.connection.execute("ALTER TABLE stores ADD COLUMN latitude REAL;")
        if "longitude" not in columns:
            self.connection.execute("ALTER TABLE stores ADD COLUMN longitude REAL;")
