"""Пресеты для KeycloakClient"""

from http import HTTPStatus

from src.user_types import KeycloakTokens

# pylint: disable=too-many-arguments, too-few-public-methods


class Presets:
    """Пресеты для Keycloak"""

    def __init__(self, client) -> None:  # noqa: ANN001
        self._client = client

    def get_token(
        self,
        username: str,
        password: str,
        client_id: str,
        client_secret: str,
        grant_type: str = "password",
        scope: str = "openid",
        realm: str | None = None,
    ) -> KeycloakTokens:
        """Авторизация в Keycloak"""
        path = {} if realm is None else {"realm": realm}
        request = self._client.post.token.path(**path).form_data(
            client_id=client_id,
            client_secret=client_secret,
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
        )
        response = request(HTTPStatus.OK, step_name="Авторизоваться в Keycloak")
        return KeycloakTokens(
            access_token=response.access_token,
            id_token=response.id_token,
            token_type=response.token_type,
        )
