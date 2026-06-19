"""Composição das dependências utilizadas pela camada web."""

import sqlite3

from app.application.product_service import ProductService
from app.application.user_service import UserService
from app.infrastructure.product_repository import SQLiteProductRepository
from app.infrastructure.user_repository import SQLiteUserRepository


def initialize_product_service(
    connection: sqlite3.Connection,
) -> ProductService:
    """AD01/US02/AD02/AD03: inicializa as dependências de produtos.

    Pré-condição: connection deve ser uma conexão SQLite aberta.
    Pós-condição: retorna o serviço com tabela e repositório configurados.
    """
    product_repository = SQLiteProductRepository(connection)
    product_repository.create_table()
    return ProductService(product_repository)


def initialize_user_service(
    connection: sqlite3.Connection,
) -> UserService:
    """US01: inicializa as dependências de autenticação.

    Pré-condição: connection deve ser uma conexão SQLite aberta.
    Pós-condição: retorna o serviço com tabela e repositório configurados.
    """
    user_repository = SQLiteUserRepository(connection)
    user_repository.create_table()
    return UserService(user_repository)
