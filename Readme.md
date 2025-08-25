# Tasks Project


## **Задача (Бизнес Задача):**
- Реализация сервиса **"Менеджер задач"**;


## Функциональные требования:
- Реализация **CRUD-операций** для управления задачами (create, get, get_list, update, delete).
- Модель задачи должна иметь в себе: uuid, название, описание, статус (создано, в работе, завершено).


## Схема взаимодействия модулей в проекте:
![Tasks_Project_Architecture](./docs/task_manager_service.png)


## Запуск проекта:
### Предварительные условия:
В зависимости от среды запуска, вам следует скопировать параметры виртуальной среды в файл **.env**(в корень проекта)
из файла [.env_examples](env_examples/.env_examples).

#### Если запуск происходит локально через **run.py**:
Примечание: при работе через **Pycharm** указать директорию **./src** как root.

1. Скопируйте параметры виртуальной среды в файл **.env**(в корень проекта). Обязательны параметры, отмеченные
**[Local]**. Вы так же можете скопировать туда все конфиги, указанные в **.env_examples_local**
(минимальный набор параметров для запуска локально)

2. Убедитесь, что **PostgreSQL** поднят у вас локально. В качестве примера можете поднять БД в **Docker-Compose
(docker-compose-services.yaml)** (указав параметры, необходимые для **[Docker_Compose]**):
```sh
docker compose -f ./docker-compose-services.yaml up -d
```

3. Установите зависимости:
```sh
pip install -r requirements.txt
```

4. Выполните миграции через **Alembic** (из директории **src**):
```sh
cd ./src
alembic upgrade head
```

5. Запустите проект:
```sh
cd ./src
uvicorn run:app --reload --port 8000
```

6. Перейдите в документацию **Swagger**: http://127.0.0.1:8000/task_manager/docs


#### Если запуск происходит через **docker-compose**:
1. Скопируйте параметры виртуальной среды в файл **.env**(в корень проекта). Обязательны параметры, отмеченные
**[Docker_Compose]**. Вы так же можете скопировать туда все конфиги, указанные в **.env_examples_docker_compose**
(минимальный набор параметров для запуска в docker-compose)

2. Запуск проекта:
```sh
docker compose -f ./docker-compose.yaml up -d
```

3. Запуск проекта с открытыми портами сервисов:
```sh
docker compose -f ./docker-compose.yaml -f docker-compose.override.yaml up -d
```

4. Перейдите в документацию **Swagger**: http://127.0.0.1:8000/task_manager/docs


## Запуск тестов:
Примечание: при работе через **Pycharm** указать директорию **./tests/functional** как root.
Проверяйте указанные параметры виртуального окружения.

#### Если запуск происходит локально:
1. Скопируйте параметры виртуальной среды в файл **.env**(в корень проекта). Вы можете скопировать туда все конфиги,
указанные в **tests/functional/.env_examples_local**
(минимальный набор параметров для запуска локально)

2. Запуск тестируемых сервисов в **docker-compose**:
```sh
cd ./tests/functional
docker compose --env-file ../../.env -f ./docker-compose-services.yaml up -d
```

3. Установка зависимостей:
```sh
cd ./tests/functional
pip install -r requirements.txt
```


#### Если запуск происходит через **docker-compose**:
1. Скопируйте параметры виртуальной среды в файл **.env**(в корень проекта). Вы можете скопировать туда все конфиги,
указанные в **tests/functional/.env_examples_docker_compose**
(минимальный набор параметров для запуска в docker-compose)

2. Запуск тестов:
```sh
cd ./tests/functional
docker compose --env-file ../../.env -f ./docker-compose.yaml up -d
```


### Запуск линтеров для локальной проверки кода:
1. Установка и обновление pre-commit (если не установлен):
```sh
pip install pre-commit
```
2. Обновление хуков до последней версии (при необходимости):
```sh
pre-commit autoupdate
```
3. Применение хук на всех файлах (например, **black**):
```sh
pre-commit run black --all-files
```
4. Очистка кэша pre-commit
```sh
pre-commit clean
```

5. Обхватить новые конфиги pre-commit
```sh
pre-commit install --overwrite
```


## Основные компоненты сервиса (исходя из технических требований):
- WebAPI: **FastAPI**(ver. 0.116.1, https://fastapi.tiangolo.com/);
- WebService: **Nginx**(ver. 1.29.0, https://nginx.org/en/docs/);
- SQLDB: **PostgreSQL**(ver. 17.5, https://www.postgresql.org/);
- Tests: **Pytest**(ver. 8.4.1, https://docs.pytest.org/);
- Others:
- - **Pydantic**(ver. 2.11.7, https://docs.pydantic.dev/);
- - **SQLAlchemyORM**(ver. 2.0.41, https://docs.sqlalchemy.org/en/20/);
- - **Alembic**(ver. 1.16.4, https://alembic.sqlalchemy.org/en/latest/);
- - **Uvicorn**(ver. 0.35.0, https://www.uvicorn.org/);


## Соглашения разработки:
### GitFlow:
#### Ветки (branches):
- **main**: основная(работоспособная) ветка кода, содержащая код для отправки на ревью;
- **develop**: рабочая ветка, содержащая актуальную кодовую базу для разработки;

#### Работа с ветками:
- Разработка нового функционала: branch: develop -> feature/....;
- Исправление ошибки в новом функционале: branch: develop(main) -> fix/...;

### REST-URI:
#### Версионирование:
- Поддержка **Stripe**-подхода (https://docs.stripe.com/api/versioning);

#### Шаблоны построения URI-методов:
- Ссылка на источник: https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api#restful


## Code Style:
- **PEP8**(https://peps.python.org/pep-0008/);
- Docstring-формат - **Epytext**(https://epydoc.sourceforge.net/manual-epytext.html);
- Linters: **Flake8**(https://flake8.pycqa.org/en/latest/);
- **Pre-commit**(https://pre-commit.com/):
- - **black** - авто-форматирование кода;
- - **flake8** - проверка стиля и ошибок;
- - **mypy** - статическая типизация;
- - **isort** - сортировка импортов;


## **Работа с Alembic:**
### Создание миграции:
```sh
alembic revision --autogenerate -m "message"
```

### Выполнение миграции:
```sh
alembic upgrade head
```

### Откат миграции на 1 шаг:
```sh
alembic downgrade -1
```


## **Осознанные допущения в проекте:**
- Местами можно заметить дубли кодовой базы: нарушение принципов разделение(точнее сказать вынесения) интерфейсов в
отдельные модули. Было бы разумно вынести это в отдельный приватный PyPi-репозиторий или иным
способом вынести их, но в рамках данного проекта было решено оставить данную связанность.
- Дубли операций в тестах (например, удаление созданных сущностей) - сделано осознано, в дальнейшем можно вынести.
