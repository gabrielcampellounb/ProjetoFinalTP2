"""Serializadores compartilhados da camada web."""


def serialize_product(product, quantity: int) -> dict:
    """AD01/US02/US04: converte produto e quantidade para JSON.

    Pré-condição: product deve expor os atributos públicos do catálogo.
    Pós-condição: retorna um dicionário serializável sem alterar o produto.
    """
    return {
        "name": product.name,
        "brand": product.brand,
        "price": product.price,
        "bar_code": product.bar_code,
        "quantity": quantity,
    }
