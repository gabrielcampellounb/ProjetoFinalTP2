"""Rotas HTTP de autenticação."""

from flask import Blueprint, jsonify, request, session

from app.application.user_service import UserService


def create_auth_blueprint(user_service: UserService) -> Blueprint:
    """US01: cria as rotas de cadastro, login e logout.

    Pré-condição: user_service deve implementar cadastro e autenticação.
    Pós-condição: retorna uma blueprint com as rotas /auth registradas.
    """
    blueprint = Blueprint("auth", __name__, url_prefix="/auth")

    @blueprint.post("/register")
    def register_user():
        """US01: cadastra um usuário comum.

        Pré-condição: o JSON deve conter nome, e-mail e senha válidos.
        Pós-condição: retorna o usuário criado com HTTP 201.
        """
        data = request.get_json()
        user = user_service.create_user(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            role="user",
        )
        return jsonify(_serialize_user(user)), 201

    @blueprint.post("/login")
    def login_user():
        """US01: autentica o usuário e cria sua sessão.

        Pré-condição: o JSON deve conter e-mail e senha.
        Pós-condição: grava user_id e role na sessão e retorna HTTP 200.
        """
        data = request.get_json()
        user = user_service.authenticate_user(
            email=data["email"],
            password=data["password"],
        )
        session.clear()
        session["user_id"] = user.user_id
        session["role"] = user.role
        return jsonify(_serialize_user(user)), 200

    @blueprint.post("/logout")
    def logout_user():
        """US01: encerra a sessão atual.

        Pré-condição: nenhuma.
        Pós-condição: limpa a sessão e retorna HTTP 204.
        """
        session.clear()
        return "", 204

    return blueprint


def _serialize_user(user) -> dict:
    """US01: converte usuário para resposta JSON sem expor o hash."""
    return {
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }
