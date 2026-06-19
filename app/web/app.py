"""Fábrica da aplicação Flask."""

import os
import sqlite3

from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest

from app.domain.exceptions import (
    DuplicateBarcodeError,
    DuplicateEmailError,
    InvalidCredentialsError,
    InvalidProductError,
    InvalidQuantityError,
    InvalidUserError,
    ProductNotFoundError,
)
from app.web.auth_routes import create_auth_blueprint
from app.web.dependencies import (
    initialize_product_service,
    initialize_user_service,
)
from app.web.routes import create_product_blueprint


def create_app(connection: sqlite3.Connection) -> Flask:
    """AD01/US01/US02/AD02/AD03: cria a aplicação Flask.

    Pré-condição: connection deve ser uma conexão SQLite aberta.
    Pós-condição: retorna a aplicação com produtos e autenticação configurados.
    """
    flask_app = Flask(__name__)
    flask_app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "development-secret-key",
    )
    product_service = initialize_product_service(connection)
    user_service = initialize_user_service(connection)

    flask_app.register_blueprint(
        create_product_blueprint(product_service)
    )
    flask_app.register_blueprint(create_auth_blueprint(user_service))
    _register_error_handlers(flask_app)

    return flask_app


def _register_error_handlers(flask_app: Flask) -> None:
    """AD01/US01/AD02: registra respostas HTTP para erros esperados."""

    @flask_app.errorhandler(InvalidProductError)
    @flask_app.errorhandler(InvalidQuantityError)
    @flask_app.errorhandler(InvalidUserError)
    def handle_validation_error(error):
        return jsonify({"erro": str(error)}), 400

    @flask_app.errorhandler(DuplicateBarcodeError)
    @flask_app.errorhandler(DuplicateEmailError)
    def handle_duplicate_bar_code(error):
        return jsonify({"erro": str(error)}), 409

    @flask_app.errorhandler(InvalidCredentialsError)
    def handle_invalid_credentials(error):
        return jsonify({"erro": str(error)}), 401

    @flask_app.errorhandler(ProductNotFoundError)
    def handle_product_not_found(error):
        return jsonify({"erro": str(error)}), 404

    @flask_app.errorhandler(BadRequest)
    def handle_bad_request(error):
        return jsonify(
            {"erro": "O corpo da requisição deve conter JSON válido."}
        ), 400

    @flask_app.errorhandler(KeyError)
    def handle_missing_field(error):
        field_name = error.args[0]
        return jsonify({"erro": f"O campo '{field_name}' é obrigatório."}), 400
