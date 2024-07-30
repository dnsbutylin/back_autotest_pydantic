"""Конфигурационный файл"""

# pylint: disable=redefined-outer-name
import logging
from pathlib import Path

import pytest
import urllib3
from environs import Env
from marshmallow.validate import URL
from pytest import Function

from clients import KeycloakClient, OlaClient, SparkClient
from src.db_client import DataBaseClient
from src.user_types import DBSettings, KeycloakSettings, KeycloakTokens, ServiceSettings, SparkSettings, UserCredentials

for i in ("faker.factory",):
    logging.getLogger(i).setLevel(level=logging.ERROR)

urllib3.disable_warnings()

logger = logging.getLogger("pytest")


# pytest hooks


def pytest_runtest_call(item: Function) -> None:
    """Start test logging"""
    logger.debug(f"Test started: {item.nodeid}")


def pytest_runtest_teardown(item: Function) -> None:
    """End test logging"""
    logger.debug(f"Test finished: {item.nodeid}")


# Configs
@pytest.fixture(scope="session")
def root_path() -> Path:
    """Возвращает путь до корневой папки"""
    return Path(__file__).parent.absolute()


@pytest.fixture(scope="session")
def _env() -> Env:
    """Чтение .env файла"""
    env = Env()
    env.read_env()
    return env


@pytest.fixture(scope="session")
def keycloak_settings(_env: Env) -> KeycloakSettings:
    """Настройки для keycloak"""
    with _env.prefixed("KEYCLOAK_"):
        return KeycloakSettings(host=_env.str("HOST", validate=URL()), realm=_env.str("REALM"))


@pytest.fixture(scope="session")
def service_settings(_env: Env) -> ServiceSettings:
    """Настройки для Ola"""
    with _env.prefixed("OLA_"):
        return ServiceSettings(
            host=_env.str("HOST", validate=URL()),
        )


@pytest.fixture(scope="session")
def user_credentials(_env: Env) -> UserCredentials:
    """Данные для авторизации"""
    with _env.prefixed("AUTH_"):
        return UserCredentials(
            keycloak_client_id=_env.str("KEYCLOAK_CLIENT_ID"),
            keycloak_client_secret=_env.str("KEYCLOAK_CLIENT_SECRET"),
            username=_env.str("USERNAME"),
            password=_env.str("PASSWORD"),
        )


@pytest.fixture(scope="session")
def db_config(_env: Env) -> DBSettings:
    """Настройки базы"""
    with _env.prefixed("DATABASE_"):
        return DBSettings(
            host=_env.str("HOST"),
            port=_env.int("PORT"),
            name=_env.str("NAME"),
            user=_env.str("USER"),
            password=_env.str("PASSWORD"),
        )


@pytest.fixture(scope="session")
def spark_config(_env: Env) -> SparkSettings:
    """Настройки СПАРКа"""
    with _env.prefixed("SPARK_"):
        return SparkSettings(
            host=_env.str("HOST"),
            login=_env.str("LOGIN"),
            password=_env.str("PASSWORD"),
        )


@pytest.fixture(scope="module")
def ola_client(service_settings: ServiceSettings) -> OlaClient:  # type:ignore[misc]
    """Получить API клиент для OLA"""
    with OlaClient(host=service_settings.host) as session:
        yield session


@pytest.fixture(scope="module")
def keycloak_client(keycloak_settings: KeycloakSettings) -> KeycloakClient:  # type:ignore[misc]
    """Модульная фикстура для получения keycloak клиента"""
    with KeycloakClient(
        host=keycloak_settings.host,
        default_path={"realm": keycloak_settings.realm},
    ) as session:
        yield session


@pytest.fixture(scope="module")
def keycloak_token(keycloak_client: KeycloakClient, user_credentials: UserCredentials) -> KeycloakTokens:
    """Модульная фикстура для авторизации в keycloak"""
    return keycloak_client.presets.get_token(
        username=user_credentials.username,
        password=user_credentials.password,
        client_id=user_credentials.keycloak_client_id,
        client_secret=user_credentials.keycloak_client_secret,
    )


@pytest.fixture(scope="module")
def auth_ola_client(ola_client: OlaClient, keycloak_token: KeycloakTokens) -> OlaClient:
    """Авторизованная сессия OLA клиента"""
    ola_client.add_token(token=keycloak_token.access_token)
    return ola_client


@pytest.fixture(scope="module")
def db_client(db_config: DBSettings) -> DataBaseClient:  # type:ignore[misc]
    """Клиент базы данных"""
    with DataBaseClient(**db_config.get()) as data_base:  # type:ignore[arg-type]
        yield data_base


@pytest.fixture(scope="module")
def spark_client(spark_config: SparkSettings) -> SparkClient:  # type:ignore[misc]
    """СПАРК клиент"""
    with SparkClient(host=spark_config.host) as client:
        client.set_auth_data(login=spark_config.login, password=spark_config.password)
        yield client
