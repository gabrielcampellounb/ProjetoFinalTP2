"""Rotas HTTP do histórico de preços por local."""

from flask import Blueprint, jsonify, request, session

from app.application.product_price_service import ProductPriceService
from app.web.authorization import authenticated_required


def create_product_price_blueprint(
    product_price_service: ProductPriceService,
) -> Blueprint:
    """US06: cria as rotas de preços com o serviço injetado.

    Pré-condição: o serviço deve permitir registro e consulta de preços.
    Pós-condição: retorna uma blueprint com as rotas de preços.
    """
    blueprint = Blueprint("product_prices", __name__)

    @blueprint.post("/prices")
    @authenticated_required
    def register_price():
        """US06: registra o preço informado pelo usuário autenticado.

        Pré-condição: sessão válida e JSON com produto, local e preço.
        Pós-condição: retorna o registro criado com HTTP 201.
        """
        data = request.get_json()
        product_price = product_price_service.register_price(
            product_bar_code=data["product_bar_code"],
            store_id=data["store_id"],
            user_id=session["user_id"],
            price=data["price"],
        )
        return jsonify(_serialize_product_price(product_price)), 201

    @blueprint.get("/products/<bar_code>/prices")
    @authenticated_required
    def list_product_prices(bar_code):
        """US06: consulta o histórico de preços de um produto.

        Pré-condição: sessão válida e produto existente.
        Pós-condição: retorna os preços observados com HTTP 200.
        """
        prices = product_price_service.list_product_prices(bar_code)
        return jsonify(
            [_serialize_product_price(product_price) for product_price in prices]
        ), 200

    return blueprint


def _serialize_product_price(product_price) -> dict:
    """US06: converte um preço observado para resposta JSON."""
    return {
        "product_bar_code": product_price.product_bar_code,
        "store_id": product_price.store_id,
        "user_id": product_price.user_id,
        "price": product_price.price,
        "created_at": product_price.created_at.isoformat(),
    }
