# Tasks Project


## **Задача (Бизнес Задача):**
- Реализация сервиса **"Менеджер задач"**;


## Функциональные требования:
- Реализация **CRUD-операций** для управления задачами (create, get, get_list, update, delete).
- Модель задачи должна иметь в себе: uuid, название, описание, статус (создано, в работе, завершено).


## Основные компоненты сервиса (исходя из технических требований):
- WebAPI: **FastAPI**(ver. 0.116.1, https://fastapi.tiangolo.com/);
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