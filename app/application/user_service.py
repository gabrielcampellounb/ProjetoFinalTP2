"""Casos de uso relacionados a usuários."""

from werkzeug.security import generate_password_hash

from app.domain.exceptions import DuplicateEmailError, InvalidUserError
from app.domain.user import User


class UserService:
    """US01: coordena o cadastro seguro de usuários."""

    def __init__(self, user_repository) -> None:
        """Inicializa o serviço de usuários.

        Pré-condição: user_repository deve implementar busca e inclusão.
        Pós-condição: o serviço fica pronto para cadastrar usuários.
        """
        self.user_repository = user_repository

    def create_user(
        self,
        name: str,
        email: str,
        password: str,
        role: str = "user",
    ) -> User:
        """US01: cria e persiste um usuário com senha protegida.

        Pré-condição: os dados devem ser válidos e o e-mail deve ser único.
        Pós-condição: retorna o usuário salvo sem armazenar a senha original.
        """
        self._validate_password(password)
        password_hash = generate_password_hash(password)
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            role=role,
        )

        if self.user_repository.get_user_by_email(user.email) is not None:
            raise DuplicateEmailError(
                f"Já existe um usuário com o e-mail {user.email}."
            )

        self.user_repository.add_user(user)
        return user

    @staticmethod
    def _validate_password(password: str) -> None:
        """US01: valida a senha recebida antes de gerar o hash."""
        if not isinstance(password, str) or not password:
            raise InvalidUserError(
                "A senha do usuário não pode estar vazia."
            )
