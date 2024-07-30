"""Функции"""

import re
from datetime import datetime
from difflib import SequenceMatcher

import allure
from box import Box

from src.cases import step


@allure.step("Сравнить строки")
def compare_string(value1: str, value2: str, min_ratio: float = 0.8) -> None:
    """
    Мягкое сравнение строк
    :param value1: Первая строка для сравнения
    :param value2: Вторая строка для сравнения
    :param min_ratio: Минимальная разница между строк (1.0 строки должны быть идентичны)
    """
    matcher = SequenceMatcher(None, tuple(value1), tuple(value2))
    assert matcher.ratio() >= min_ratio, f"{value1} != {value2}"


def get_datetime_format(str_date: str) -> str:
    """Получить формат даты"""
    if re.match(r"^\d{2}\.\d{2}\.\d{4}$", str_date):
        return "%d.%m.%Y"
    if re.match(r"^\d{4}-\d{2}-\d{2}$", str_date):
        return "%Y-%m-%d"
    if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", str_date):
        return "%Y-%m-%dT%H:%M:%SZ"
    raise ValueError(f"Not found format by date: '{str_date}'")


def get_datetime(str_date: str) -> datetime | str:
    """Получить объект datetime из строки"""
    if str_date == "":
        return str_date
    datetime_format = get_datetime_format(str_date)
    return datetime.strptime(str_date, datetime_format)


@allure.step("Проверить, что данные компании из API соответствуют данным из СПАРКа")
def compare_spark_company(spark_data: Box, api_data: Box) -> None:
    """Сравнить данные из спарка"""
    with step("ИНН соответствует значению в СПАРКе"):
        assert api_data.inn == spark_data.inn
    with step("ОГРН соответствует значению в СПАРКе"):
        assert api_data.ogrn == spark_data.ogrn
    with step("Сокращенное название соответствует значению в СПАРКе"):
        assert api_data.short_name == spark_data.get("shortNameRus")
    with step("Полное название соответствует значению в СПАРКе"):
        assert api_data.full_name == spark_data.get("fullNameRus")
    with step("Дата рагистрации соответствует значению в СПАРКе"):
        assert get_datetime(api_data.registration_date) == get_datetime(spark_data.dateFirstReg)
    with step("Email соответствует значению в СПАРКе"):
        assert api_data.email == spark_data.get("email")
    with step("Website соответствует значению в СПАРКе"):
        assert api_data.website == spark_data.get("www")
    with step("Staff_number соответствует значению в СПАРКе"):
        if staff := spark_data.get("staffNumberFTS"):
            staff_number = staff[0].number
        else:
            staff_number = None
        assert api_data.staff_number == staff_number
    charter_capital = spark_data.get("charterCapital", {})
    with step("authorized_capital.actual_date соответствует значению в СПАРКе"):
        assert get_datetime(api_data.authorized_capital.actual_date) == get_datetime(
            charter_capital.get("actualDate", ""),
        )
    with step("authorized_capital.value соответствует значению в СПАРКе"):
        assert api_data.authorized_capital.value == charter_capital.get("value", 0)
    with step("okfs соответствует значению в СПАРКе"):
        assert api_data.okfs == spark_data.get("okfs")
    with step("main_okved.code соответствует значению в СПАРКе"):
        assert api_data.main_okved.code == spark_data.okved2List[0].code
    with step("main_okved.name соответствует значению в СПАРКе"):
        assert api_data.main_okved.name == spark_data.okved2List[0].name


@allure.step("Проверить, что данные ИП из API соответствуют данным из СПАРКа")
def compare_spark_ip(spark_data: Box, api_data: Box) -> None:
    """Сравнить данные из спарка"""
    with step("ИНН соответствует значению в СПАРКе"):
        assert api_data.inn == spark_data.inn
    with step("ОГРН соответствует значению в СПАРКе"):
        assert api_data.ogrn == spark_data.ogrnip
    with step("Сокращенное название соответствует значению в СПАРКе"):
        assert api_data.short_name == spark_data.get("fullNameRus")
    with step("Полное название соответствует значению в СПАРКе"):
        assert api_data.full_name == spark_data.get("fullNameRus")
    with step("Email соответствует значению в СПАРКе"):
        assert api_data.email == spark_data.get("email")
    with step("Website соответствует значению в СПАРКе"):
        assert api_data.website == spark_data.get("www")
    with step("Staff_number null"):
        assert api_data.staff_number is None

    with step("authorized_capital.actual_date содержит пустую строку"):
        assert api_data.authorized_capital.actual_date == ""
    with step("authorized_capital.value равен 0"):
        assert api_data.authorized_capital.value == 0
    with step("okfs.code содержит пустую строку"):
        assert api_data.okfs.code == ""
    with step("okfs.name содержит пустую строку"):
        assert api_data.okfs.name == ""
    with step("main_okved.code соответствует значению в СПАРКе"):
        assert api_data.main_okved.code == spark_data.okved2List[0].code
    with step("main_okved.name соответствует значению в СПАРКе"):
        assert api_data.main_okved.name == spark_data.okved2List[0].name
