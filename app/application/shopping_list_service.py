"""Casos de uso relacionados a listas de compras."""

from datetime import datetime, timezone
from typing import Callable

from app.domain.shopping_list import ShoppingList


class ShoppingListService:
    """US03: coordena a criação de listas de compras."""

    def __init__(
        self,
        shopping_list_repository,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Inicializa o serviço de listas de compras.

        Pré-condição: o repositório deve implementar inclusão de listas.
        Pós-condição: o serviço fica pronto para criar listas.
        """
        self.shopping_list_repository = shopping_list_repository
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def create_shopping_list(
        self,
        user_id: int,
        name: str,
    ) -> ShoppingList:
        """US03: cria uma lista associada ao usuário autenticado.

        Pré-condição: user_id e name devem ser válidos.
        Pós-condição: retorna a lista criada e persistida.
        """
        shopping_list = ShoppingList(
            list_id=None,
            user_id=user_id,
            name=name,
            created_at=self.clock(),
        )
        self.shopping_list_repository.add_shopping_list(shopping_list)
        return shopping_list
