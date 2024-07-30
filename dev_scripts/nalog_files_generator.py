"""
Скрипт для облегчения сбора данных по компаниям с сайта https://egrul.nalog.ru/index.html
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Final

ROOT_PATH: Final[Path] = Path(__file__).parent.parent.absolute()
FIND_DIR: Final[Path] = ROOT_PATH / "nalog_files"
FINAL_FILE: Final[Path] = ROOT_PATH / "files" / "comp.json"

MIN_REG_DATE: datetime = datetime(2022, 5, 31)


class Keys:
    LIQUIDATION_DATE = "e"
    REGISTRATION_DATE = "r"


def main() -> None:  # noqa: CCR001
    data = []
    for path in FIND_DIR.glob("*.json"):
        print(f"Read: {path}")
        with path.open("rb") as file:
            values = json.loads(file.read())
        if "rows" in values:
            values = values["rows"]
        for row in values:
            if Keys.LIQUIDATION_DATE not in row:
                if ref_date := row.get(Keys.REGISTRATION_DATE, None):
                    if datetime.strptime(ref_date, "%d.%m.%Y") <= MIN_REG_DATE:
                        data.append(row)

    print(f"Write: {len(data)} companies")
    with FINAL_FILE.open("wb") as final_file:
        final_file.write(json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8"))


if __name__ == "__main__":
    main()
