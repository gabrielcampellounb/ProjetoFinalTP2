"""Caso de uso das métricas administrativas."""


class AdminMetricsService:
    """AD04: coordena a consulta das métricas administrativas."""

    def __init__(self, metrics_repository) -> None:
        """AD04: inicializa o serviço de métricas.

        Pré-condição: o repositório deve fornecer get_metrics.
        Pós-condição: o serviço fica pronto para consultar os totais.
        """
        self.metrics_repository = metrics_repository

    def get_metrics(self) -> dict[str, int]:
        """AD04: consulta os totais administrativos.

        Pré-condição: o repositório deve estar configurado.
        Pós-condição: retorna as métricas persistidas no SQLite.
        """
        return self.metrics_repository.get_metrics()
