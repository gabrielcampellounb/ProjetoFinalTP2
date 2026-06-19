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

    @blueprint.post("/shopping-lists/<int:list_id>/items")
    @authenticated_required
    def add_item(list_id):
        """US03: adiciona um produto à lista do usuário autenticado.

        Pré-condição: sessão, lista própria, produto e quantidade válidos.
        Pós-condição: retorna o item criado com HTTP 201.
        """
        data = request.get_json()
        item = shopping_list_service.add_item(
            user_id=session["user_id"],
            list_id=list_id,
            bar_code=data["bar_code"],
            quantity=data["quantity"],
        )
        return jsonify(_serialize_item(item)), 201

    @blueprint.patch("/shopping-lists/<int:list_id>/items/<bar_code>")
    @authenticated_required
    def update_item(list_id, bar_code):
        """US03: altera a quantidade de um item da lista própria.

        Pré-condição: sessão, lista própria, item e quantidade válidos.
        Pós-condição: retorna o item atualizado com HTTP 200.
        """
        data = request.get_json()
        item = shopping_list_service.update_item(
            user_id=session["user_id"],
            list_id=list_id,
            bar_code=bar_code,
            quantity=data["quantity"],
        )
        return jsonify(_serialize_item(item)), 200

    @blueprint.delete("/shopping-lists/<int:list_id>/items/<bar_code>")
    @authenticated_required
    def remove_item(list_id, bar_code):
        """US03: remove um item existente da lista própria.

        Pré-condição: sessão autenticada, lista própria e item existente.
        Pós-condição: remove o item e retorna HTTP 204.
        """
        shopping_list_service.remove_item(
            user_id=session["user_id"],
            list_id=list_id,
            bar_code=bar_code,
        )
        return "", 204

    return blueprint


def _serialize_shopping_list(shopping_list) -> dict:
    """US03: converte uma lista de compras para resposta JSON."""
    return {
        "id": shopping_list.list_id,
        "user_id": shopping_list.user_id,
        "name": shopping_list.name,
        "created_at": shopping_list.created_at.isoformat(),
    }


def _serialize_item(item) -> dict:
    """US03: converte um item de lista para resposta JSON."""
    return {
        "list_id": item.list_id,
        "bar_code": item.bar_code,
        "quantity": item.quantity,
    }
