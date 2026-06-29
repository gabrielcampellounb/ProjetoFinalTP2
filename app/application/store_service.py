"""Casos de uso relacionados a locais de compra."""

from geopy.distance import geodesic

from app.domain.exceptions import InvalidStoreError, StoreNotFoundError
from app.domain.store import Store


class StoreService:
    """US06: coordena cadastro e consulta de locais de compra."""

    def __init__(self, store_repository) -> None:
        """Inicializa o serviço de locais.

        Pré-condição: o repositório deve implementar inclusão e listagem.
        Pós-condição: o serviço fica pronto para gerenciar locais.
        """
        self.store_repository = store_repository

    def create_store(
        self,
        name: str,
        address: str,
        observation: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> Store:
        """US06: cria e persiste um local de compra.

        Pré-condição: dados e coordenadas opcionais devem ser válidos.
        Pós-condição: retorna o local criado e persistido.
        """
        store = Store(
            store_id=None,
            name=name,
            address=address,
            observation=observation,
            latitude=latitude,
            longitude=longitude,
        )
        self.store_repository.add_store(store)
        return store

    def list_stores(self) -> list[Store]:
        """US06: lista os locais de compra disponíveis.

        Pré-condição: o repositório deve estar inicializado.
        Pós-condição: retorna todos os locais ordenados pelo repositório.
        """
        return self.store_repository.list_stores()

    def get_store(self, store_id: int) -> Store | None:
        """US06/WEB: consulta um local pelo identificador.

        Pré-condição: store_id deve identificar o local procurado.
        Pós-condição: retorna o local encontrado ou None.
        """
        return self.store_repository.get_store_by_id(store_id)

    def find_nearest_store(
        self, latitude: float, longitude: float
    ) -> tuple[Store, float]:
        """US06/GPS: encontra a loja geolocalizada mais próxima.

        Pré-condição: latitude e longitude devem representar a posição do usuário.
        Pós-condição: retorna a loja mais próxima e a distância em quilômetros.
        """
        user_location = self._validate_user_location(latitude, longitude)
        nearest_store = None
        nearest_distance = None
        for store in self.store_repository.list_stores():
            if store.latitude is None or store.longitude is None:
                continue
            distance_km = geodesic(
                user_location,
                (store.latitude, store.longitude),
            ).kilometers
            if nearest_distance is None or distance_km < nearest_distance:
                nearest_store = store
                nearest_distance = distance_km

        if nearest_store is None or nearest_distance is None:
            raise StoreNotFoundError(
                "Nenhum local de compra com coordenadas foi encontrado."
            )
        return nearest_store, round(nearest_distance, 3)

    @staticmethod
    def _validate_user_location(
        latitude: float, longitude: float
    ) -> tuple[float, float]:
        """US06/GPS: valida a posição recebida do GPS do usuário.

        Pré-condição: latitude e longitude devem ser valores numéricos.
        Pós-condição: retorna a coordenada validada ou lança InvalidStoreError.
        """
        try:
            normalized_latitude = float(latitude)
            normalized_longitude = float(longitude)
        except (TypeError, ValueError) as error:
            raise InvalidStoreError(
                "Latitude e longitude devem ser numéricas."
            ) from error

        Store(
            store_id=None,
            name="Referência GPS",
            address="Coordenada do usuário",
            latitude=normalized_latitude,
            longitude=normalized_longitude,
        )
        return normalized_latitude, normalized_longitude
