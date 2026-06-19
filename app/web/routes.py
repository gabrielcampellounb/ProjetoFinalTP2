"""Rotas HTTP da aplicação."""

from flask import Blueprint, jsonify, request

from app.application.product_service import ProductService


def create_product_blueprint(
    product_service: ProductService,
) -> Blueprint:
    """AD01: cria a rota de cadastro com o serviço injetado.

    Pré-condição: product_service deve permitir a criação de produtos.
    Pós-condição: retorna uma blueprint com POST /products registrado.
    """
    blueprint = Blueprint("products", __name__)

    @blueprint.post("/products")
    def create_product():
        """AD01: cria um produto a partir dos dados JSON recebidos.

        Pré-condição: a requisição deve conter os campos obrigatórios.
        Pós-condição: retorna o produto criado em JSON com HTTP 201.
        """
        data = request.get_json()
        product = product_service.create_product(
            name=data["name"],
            brand=data["brand"],
            price=data["price"],
            bar_code=data["bar_code"],
            quantity=data["quantity"],
        )

        return jsonify(_serialize_product(product, data["quantity"])), 201

    @blueprint.get("/products")
    def search_products():
        """US02: busca produtos por nome ou marca.

        Pré-condição: o parâmetro opcional q contém o texto da busca.
        Pós-condição: retorna uma lista JSON e HTTP 200.
        """
        query = request.args.get("q", "")
        results = product_service.search_products(query)

        return jsonify(
            [
                _serialize_product(product, quantity)
                for product, quantity in results
            ]
        ), 200

    return blueprint


def _serialize_product(product, quantity: int) -> dict:
    """AD01/US02: converte produto e quantidade para resposta JSON."""
    return {
        "name": product.name,
        "brand": product.brand,
        "price": product.price,
        "bar_code": product.bar_code,
        "quantity": quantity,
    }
