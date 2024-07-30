# OLA Backend autotests

API тесты OLA

## Зависимости

* Python: 3.11+
* Pip: 22.3.1+
* Poetry 1.3.2+

## Ссылки:

* [Bitbucket](https://git.ucb.local/projects/OLA/repos/ola_backend_autotests/browse)
* [Jira project](https://jira.ucb.local/projects/OLAF/summary)
* [Allure](https://allure.ucb.local/project/39/)
* [Bamboo linters](https://bamboo.ucb.local/browse/UCCT-OBL)

---

## Использование script.py

#### Установка

* Зависимости для запуска тестов
    ```shell
    python script.py install
    ```

* Зависимости для написания тестов
    ```shell
    python script.py install --all
    ```

#### Удаление проекта

```shell
python script.py remove
```

#### Форматирование кода

```shell
python script.py format
```

#### Запуск линтеров

```shell
python script.py lint
```

#### Копирование .env файла из .env.example

```shell
python script.py copy-env
```

#### Генерация .env файла для bamboo

```shell
python script.py bamboo-env
```

#### Генерация .pyi файлов

```shell
python script.py pyi
```
