"""Скрипт для сбора данных о ИП в один файл"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Final

ROOT_PATH: Final[Path] = Path(__file__).parent.parent.absolute()
FIND_DIR: Final[Path] = ROOT_PATH / "ip_files"
FINAL_FILE: Final[Path] = ROOT_PATH / "files" / "ip.json"

MIN_REG_DATE: datetime = datetime(2022, 5, 31)

MONTHS = (
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
)


class Keys:
    NAME = "name"
    INN = "ИНН"
    OGRNIP = "ОГРНИП"
    REG_DATE = "ДАТА РЕГИСТРАЦИИ"
    MAIN_ACTIVITY = "ОСНОВНОЙ ВИД ДЕЯТЕЛЬНОСТИ"


def main() -> None:  # noqa: CCR001
    data = []
    for path in FIND_DIR.glob("*.json"):
        print(f"Read: {path}")
        with path.open("rb") as file:
            values = json.loads(file.read())
        for item in values:
            if match := re.match(
                r"^(?P<day>\d{1,2})\s(?P<month>[а-яА-Я]+)\s(?P<year>\d{4})", item.get(Keys.REG_DATE, "")
            ):
                _date = match.groupdict()
                index = MONTHS.index(_date["month"])
                _datetime = datetime(year=int(_date["year"]), month=index + 1, day=int(_date["day"]))
                if _datetime <= MIN_REG_DATE:
                    value = {
                        "name": item.get(Keys.NAME),
                        "inn": item.get(Keys.INN),
                        "ogrnip": item.get(Keys.OGRNIP),
                        "reg": _datetime.strftime("%d.%m.%Y"),
                        "activity": item.get(Keys.MAIN_ACTIVITY, ""),
                    }
                    if all([i is not None for i in value.values()]):
                        data.append(value)
    print(f"Write: {len(data)} ip")
    with FINAL_FILE.open("wb") as final_file:
        final_file.write(json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8"))


if __name__ == "__main__":
    main()
