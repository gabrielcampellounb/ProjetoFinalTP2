"""Rotas HTTP de listas de compras."""

from flask import Blueprint, jsonify, request, session

from app.application.shopping_list_service import ShoppingListService
from app.web.authorization import authenticated_required


def create_shopping_list_blueprint(
    shopping_list_service: ShoppingListService,
) -> Blueprint:
    """US03: cria as rotas de listas com o serviço injetado.

    Pré-condição: o serviço deve permitir a criação de listas.
    Pós-condição: retorna uma blueprint com POST /shopping-lists.
    """
    blueprint = Blueprint("shopping_lists", __name__)

    @blueprint.post("/shopping-lists")
    @authenticated_required
    def create_shopping_list():
        """US03: cria uma lista para o usuário autenticado.

        Pré-condição: sessão autenticada e JSON com name válido.
        Pós-condição: retorna a lista criada com HTTP 201.
        """
        data = request.get_json()
        shopping_list = shopping_list_service.create_shopping_list(
            user_id=session["user_id"],
            name=data["name"],
        )
        return jsonify(_serialize_shopping_list(shopping_list)), 201

    return blueprint


def _serialize_shopping_list(shopping_list) -> dict:
    """US03: converte uma lista de compras para resposta JSON."""
    return {
        "id": shopping_list.list_id,
        "user_id": shopping_list.user_id,
        "name": shopping_list.name,
        "created_at": shopping_list.created_at.isoformat(),
    }
