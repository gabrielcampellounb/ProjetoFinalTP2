"""Rotas HTTP da aplicação."""

from flask import Blueprint, jsonify, request


def create_product_blueprint(product_service) -> Blueprint:
    """Cria as rotas de produtos com o serviço injetado.

    Pré-condição: product_service deve permitir a criação de produtos.
    Pós-condição: retorna uma blueprint com POST /products registrado.
    """
    blueprint = Blueprint("products", __name__)

    @blueprint.post("/products")
    def create_product():
        """Cria um produto a partir dos dados JSON recebidos."""
        data = request.get_json()
        product = product_service.create_product(
            name=data["name"],
            brand=data["brand"],
            price=data["price"],
            bar_code=data["bar_code"],
            quantity=data["quantity"],
        )

        return jsonify(
            {
                "name": product.name,
                "brand": product.brand,
                "price": product.price,
                "bar_code": product.bar_code,
                "quantity": data["quantity"],
            }
        ), 201

    return blueprint
