"""Entidades e regras de validação de produtos."""

from app.domain.exceptions import InvalidProductError


class Product:
    """Representa um produto com atributos sempre válidos."""

    BAR_CODE_LENGTH = 13

    def __init__(
        self,
        name: str,
        brand: str,
        price: int | float,
        bar_code: str,
    ) -> None:
        """Cria um produto.

        Pré: os argumentos devem atender às regras de cada atributo.
        Pós: o produto é inicializado ou InvalidProductError é lançada.
        """
        self.name = name
        self.brand = brand
        self.price = price
        self.bar_code = bar_code

    @property
    def name(self) -> str:
        """Retorna o nome válido armazenado."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Atualiza o nome.

        Pré: value deve ser uma string não vazia.
        Pós: o nome é atualizado ou InvalidProductError é lançada.
        """
        self._validate_text(value, "name")
        self._name = value

    @property
    def brand(self) -> str:
        """Retorna a marca válida armazenada."""
        return self._brand

    @brand.setter
    def brand(self, value: str) -> None:
        """Atualiza a marca.

        Pré: value deve ser uma string não vazia.
        Pós: a marca é atualizada ou InvalidProductError é lançada.
        """
        self._validate_text(value, "brand")
        self._brand = value

    @property
    def price(self) -> int | float:
        """Retorna o preço válido armazenado."""
        return self._price

    @price.setter
    def price(self, value: int | float) -> None:
        """Atualiza o preço.

        Pré: value deve ser numérico e não negativo.
        Pós: o preço é atualizado ou InvalidProductError é lançada.
        """
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidProductError("Product price must be a number.")
        if value < 0:
            raise InvalidProductError("Product price cannot be negative.")
        self._price = value

    @property
    def bar_code(self) -> str:
        """Retorna o código de barras válido armazenado."""
        return self._bar_code

    @bar_code.setter
    def bar_code(self, value: str) -> None:
        """Atualiza o código de barras.

        Pré: value deve conter exatamente 13 dígitos ASCII.
        Pós: o código é atualizado ou InvalidProductError é lançada.
        """
        if not isinstance(value, str):
            raise InvalidProductError("Product bar code must be a string.")
        if (
            len(value) != self.BAR_CODE_LENGTH
            or not value.isascii()
            or not value.isdigit()
        ):
            raise InvalidProductError("Product bar code must be a string of 13 digits.")
        self._bar_code = value

    @staticmethod
    def _validate_text(value: str, field_name: str) -> None:
        """Valida um campo textual.

        Pré: field_name identifica o campo recebido.
        Pós: retorna sem efeito ou lança InvalidProductError.
        """
        if not isinstance(value, str):
            raise InvalidProductError(
                f"Product {field_name} must be a string."
            )
        if not value:
            raise InvalidProductError(
                f"Product {field_name} cannot be empty."
            )
