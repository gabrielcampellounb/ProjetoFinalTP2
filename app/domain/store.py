"""Entidade e regras de validação de locais de compra."""

from app.domain.exceptions import InvalidStoreError


class Store:
    """US06: representa um local de compra disponível."""

    def __init__(
        self,
        store_id: int | None,
        name: str,
        address: str,
        observation: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> None:
        """US06: cria um local de compra validado.

        Pré-condição: nome, endereço e coordenadas opcionais devem ser válidos.
        Pós-condição: cria o local ou lança InvalidStoreError.
        """
        self.store_id = self._validate_store_id(store_id)
        self.name = self._validate_required_text(name, "nome")
        self.address = self._validate_required_text(address, "endereço")
        self.observation = self._validate_observation(observation)
        self.latitude = self._validate_coordinate(
            value=latitude,
            field_name="latitude",
            minimum=-90,
            maximum=90,
        )
        self.longitude = self._validate_coordinate(
            value=longitude,
            field_name="longitude",
            minimum=-180,
            maximum=180,
        )
        if (self.latitude is None) != (self.longitude is None):
            raise InvalidStoreError("Latitude e longitude devem ser informadas juntas.")

    @staticmethod
    def _validate_store_id(store_id: int | None) -> int | None:
        """US06: valida o identificador opcional do local."""
        if store_id is None:
            return None
        if isinstance(store_id, bool) or not isinstance(store_id, int):
            raise InvalidStoreError(
                "O identificador do local deve ser um número inteiro."
            )
        return store_id

    @staticmethod
    def _validate_required_text(value: str, field_name: str) -> str:
        """US06: valida um campo textual obrigatório."""
        if not isinstance(value, str) or not value.strip():
            raise InvalidStoreError(f"O {field_name} do local não pode estar vazio.")
        return value.strip()

    @staticmethod
    def _validate_observation(observation: str | None) -> str | None:
        """US06: valida a observação opcional do local."""
        if observation is None:
            return None
        if not isinstance(observation, str):
            raise InvalidStoreError("A observação do local deve ser uma string.")
        normalized = observation.strip()
        return normalized or None

    @staticmethod
    def _validate_coordinate(
        value: float | None,
        field_name: str,
        minimum: float,
        maximum: float,
    ) -> float | None:
        """US06/GPS: valida uma coordenada geográfica opcional.

        Pré-condição: value deve ser None ou número dentro do intervalo.
        Pós-condição: retorna float normalizado ou lança InvalidStoreError.
        """
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise InvalidStoreError(f"A {field_name} do local deve ser numérica.")
        normalized = float(value)
        if normalized < minimum or normalized > maximum:
            raise InvalidStoreError(f"A {field_name} do local está fora dos limites.")
        return normalized
