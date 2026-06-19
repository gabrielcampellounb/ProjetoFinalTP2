"""Exceções específicas das regras de produtos."""


class InvalidProductError(Exception):
    """Indica que um atributo viola uma pré-condição do produto."""


class DuplicateBarcodeError(Exception):
    """Indica que o código de barras já está cadastrado."""


class ProductNotFoundError(Exception):
    """Indica que o produto solicitado não foi encontrado."""
