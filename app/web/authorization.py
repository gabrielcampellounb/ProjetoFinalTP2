"""Regras de autorização da camada web."""

from functools import wraps

from flask import jsonify, session


def admin_required(view_function):
    """RNF02: exige uma sessão autenticada com papel de administrador.

    Pré-condição: a função decorada deve ser uma view Flask.
    Pós-condição: executa a view para admin ou retorna HTTP 401/403.
    """

    @wraps(view_function)
    def authorized_view(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"erro": "Autenticação necessária."}), 401
        if session.get("role") != "admin":
            return jsonify(
                {"erro": "Acesso permitido apenas para administradores."}
            ), 403

        return view_function(*args, **kwargs)

    return authorized_view
