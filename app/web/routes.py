"""Rotas HTTP da aplicação."""

from flask import Blueprint, jsonify, request

from app.application.product_service import ProductService


def create_product_blueprint(
    product_service: ProductService,
) -> Blueprint:
    """AD01/US02/AD02/AD03: cria as rotas com o serviço injetado.

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

    @blueprint.put("/products/<bar_code>")
    def update_product(bar_code):
        """AD02: edita um produto identificado pelo código de barras.

        Pré-condição: o produto deve existir e o JSON deve ser válido.
        Pós-condição: retorna o produto atualizado em JSON com HTTP 200.
        """
        data = request.get_json()
        product, quantity = product_service.update_product(
            bar_code=bar_code,
            name=data["name"],
            brand=data["brand"],
            price=data["price"],
        )

        return jsonify(_serialize_product(product, quantity)), 200

    @blueprint.delete("/products/<bar_code>")
    def deactivate_product(bar_code):
        """AD02: remove logicamente um produto pelo código de barras.

        Pré-condição: o código deve identificar um produto cadastrado.
        Pós-condição: desativa o produto e retorna HTTP 204 sem conteúdo.
        """
        product_service.deactivate_product(bar_code)
        return "", 204

    @blueprint.patch("/products/<bar_code>/stock")
    def update_stock(bar_code):
        """AD03: atualiza a quantidade em estoque de um produto.

        Pré-condição: o produto deve existir e o JSON conter quantity válida.
        Pós-condição: retorna produto e estoque atualizado com HTTP 200.
        """
        data = request.get_json()
        product, quantity = product_service.update_stock(
            bar_code=bar_code,
            quantity=data["quantity"],
        )

        return jsonify(_serialize_product(product, quantity)), 200

    return blueprint


def _serialize_product(product, quantity: int) -> dict:
    """AD01/US02/AD02/AD03: converte produto e estoque para resposta JSON."""
    return {
        "name": product.name,
        "brand": product.brand,
        "price": product.price,
        "bar_code": product.bar_code,
        "quantity": quantity,
    }
