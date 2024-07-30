#!/usr/bin/python3
import logging
import re
import shutil
import subprocess
import time
from argparse import ArgumentParser, Namespace
from functools import wraps
from os import environ
from pathlib import Path
from shutil import rmtree
from typing import Callable, Final

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")

# Configuration
TEMP: Final[tuple[str, ...]] = (
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    "pytest.log",
    "pytest.html",
    "report",
)
SOURCE: Final[tuple[str, ...]] = ("src", "conftest.py", "clients")

BASE_CMD: Final[tuple[str, ...]] = ("poetry", "run")
ROOT: Final[Path] = Path(".").absolute()
SOURCE_PATHS: Final[tuple[str, ...]] = tuple(str(ROOT / i) for i in SOURCE)


def get_all_py_files() -> list[str]:  # noqa:  CCR001
    """Находит все .py файлы проекта"""
    files = []
    for i in SOURCE:
        if (path := ROOT.joinpath(i)).exists():
            if path.is_file() and path.suffix == ".py":
                files.append(str(path))
            elif path.is_dir():
                files.extend([str(p) for p in path.rglob("*.py")])
    return files


ALL_PY: Final[list[str]] = get_all_py_files()


def cmd_log(func: Callable[[Namespace], None]) -> Callable[[Namespace], None]:
    """Декоратор логирования вызовов команд"""

    @wraps(func)
    def _call(args: Namespace) -> None:
        logging.info(f"run command: {args.command}")
        start = time.monotonic()
        result = func(args)
        logging.info(f"{args.command} done {round(time.monotonic() - start, 2)}s")
        return result

    return _call


class CMD:
    # lint
    FLAKE8: Final[tuple[str, ...]] = ("flake8", str(ROOT))
    MYPY: Final[tuple[str, ...]] = ("mypy", "--ignore-missing-imports", "--check-untyped-defs", str(ROOT))
    BANDIT: Final[tuple[str, ...]] = ("bandit", "-c", "pyproject.toml", "-r", str(ROOT))
    PYLINT: Final[tuple[str, ...]] = ("pylint", *SOURCE_PATHS)
    BLACK_LINT: Final[tuple[str, ...]] = ("black", str(ROOT), "--check")
    ISORT_LINT: Final[tuple[str, ...]] = ("isort", "-c", str(ROOT))
    # format
    ISORT: Final[tuple[str, ...]] = ("isort", str(ROOT))
    BLACK: Final[tuple[str, ...]] = ("black", str(ROOT))
    ADD_TRAILING_COMMA: Final[tuple[str, ...]] = (
        "add-trailing-comma",
        *ALL_PY,
        "--py36-plus",
        "--exit-zero-even-if-changed",
    )


@cmd_log
def install_command(arg: Namespace) -> None:
    """Создание env"""
    cmd = ["poetry", "install", "--no-cache", "--no-root"]
    if not arg.all:
        cmd.extend(["--only", "main"])
    subprocess.run(cmd)


@cmd_log
def remove_command(arg: Namespace) -> None:  # noqa: CCR001
    """Удаление env"""
    logging.debug("Remove tmp files")
    for file in TEMP:
        if (_file := ROOT / file).exists():
            logging.info(f"Remove: {_file}")
            if _file.is_file():
                _file.unlink(missing_ok=True)
            elif _file.is_dir():
                rmtree(_file, ignore_errors=True)
    logging.debug("Remove chromedriver")
    for i in ROOT.glob("chromedriver*"):
        i.unlink(missing_ok=True)


@cmd_log
def lint_command(arg: Namespace) -> None:
    """Запуск линтеров"""
    for lint in (
        CMD.FLAKE8,
        CMD.MYPY,
        CMD.BANDIT,
        CMD.PYLINT,
        CMD.BLACK_LINT,
        CMD.ISORT_LINT,
    ):
        logging.info(f"Run: {lint[0]}")
        process = subprocess.run(BASE_CMD + lint)
        if process.returncode != 0 and not arg.ignore:
            raise SystemExit(f"Failed: {lint[0]}")


@cmd_log
def format_command(arg: Namespace) -> None:
    """Запуск форматтеров"""
    for lint in CMD.ISORT, CMD.BLACK, CMD.ADD_TRAILING_COMMA:
        logging.info(f"Run: {lint[0]}")
        subprocess.run(BASE_CMD + lint)


@cmd_log
def copy_env(arg: Namespace) -> None:
    """Копирование env файла"""
    if (example := ROOT / ".env.example").exists():
        shutil.copy(example, ROOT / ".env")


@cmd_log
def bamboo_env(arg: Namespace) -> None:  # noqa: CCR001
    """Генерация .env файла для bamboo"""
    if (example := ROOT / arg.file).exists():
        dot_envs = []
        with example.open("rb") as ex_file:
            string = ex_file.read().decode("utf-8")
            keys = [i.groups()[0] for i in re.finditer(r"(?P<key>[0-9A-Z_]+)=", string) if i]
        for key, value in environ.items():
            env_key = key.removeprefix(arg.prefix)
            if env_key in keys:
                dot_envs.append((env_key, value))
        if dot_envs:
            file = ROOT / ".env"
            with file.open("wb") as _file:
                _file.write("\n".join([f"{k}={v}" for k, v in dot_envs]).encode("utf-8"))
    else:
        raise FileNotFoundError(f"Not found {example}")


@cmd_log
def pyi_generate(arg: Namespace) -> None:
    """Запускает генератор pyi файлов"""
    subprocess.run(BASE_CMD + ("python", str(ROOT / "dev_scripts" / "pyi_generator.py")))


parser = ArgumentParser(description="Cli скрипт для удобной настройки", prog="CLI")
subparser = parser.add_subparsers(dest="command", required=True, title="Команды")

install_parser = subparser.add_parser("install", help="Установка")
install_parser.add_argument(
    "-a",
    "--all",
    help="Установить все зависимости",
    dest="all",
    action="store_true",
)
install_parser.set_defaults(func=install_command)

remove_parser = subparser.add_parser("remove", help="Удаление")
remove_parser.set_defaults(func=remove_command)

lint_parser = subparser.add_parser("lint", help="Запуск линтеров")
lint_parser.add_argument(
    "-i",
    "--ignore",
    help="Игнорировать падения",
    dest="ignore",
    action="store_true",
)
lint_parser.set_defaults(func=lint_command)

format_parser = subparser.add_parser("format", help="Запуск форматеров")
format_parser.set_defaults(func=format_command)

copy_env_parser = subparser.add_parser("copy-env", help="Копирование env файла")
copy_env_parser.set_defaults(func=copy_env)

bamboo_env_parser = subparser.add_parser("bamboo-env", help="Генерация .env файла для bamboo")
bamboo_env_parser.add_argument(
    "-f",
    "--file",
    help="File name",
    default=".env.example",
    dest="file",
)
bamboo_env_parser.add_argument(
    "-p",
    "--prefix",
    help="ENV prefix",
    default="bamboo_",
    dest="prefix",
)
bamboo_env_parser.set_defaults(func=bamboo_env)
pyi_parser = subparser.add_parser("pyi", help="Генерация .pyi файлов")
pyi_parser.set_defaults(func=pyi_generate)

if __name__ == "__main__":
    cmd_args = parser.parse_args()
    cmd_args.func(cmd_args)
