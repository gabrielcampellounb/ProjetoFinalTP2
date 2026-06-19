"""Rotas HTTP das métricas administrativas."""

from flask import Blueprint, jsonify

from app.application.admin_metrics_service import AdminMetricsService
from app.web.authorization import admin_required


def create_admin_metrics_blueprint(
    metrics_service: AdminMetricsService,
) -> Blueprint:
    """AD04: cria a rota administrativa com o serviço injetado.

    Pré-condição: metrics_service deve permitir consulta das métricas.
    Pós-condição: retorna uma blueprint com GET /admin/metrics.
    """
    blueprint = Blueprint("admin_metrics", __name__)

    @blueprint.get("/admin/metrics")
    @admin_required
    def get_admin_metrics():
        """AD04: retorna métricas para administrador autenticado.

        Pré-condição: a sessão deve pertencer a um administrador.
        Pós-condição: retorna os totais do SQLite com HTTP 200.
        """
        return jsonify(metrics_service.get_metrics()), 200

    return blueprint
