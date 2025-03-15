# Testing-FastAPI-Server

### Структура Проекта

```
.
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .python-version
├── .gitignore
├── .dockerignore
├── app
│   ├── auth.py
│   ├── conf.py
│   ├── database.py
│   ├── main.py
│   ├── applications
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── review.py
│   │   ├── task.py
│   │   └── user.py
│   ├── mapper
│   │   └── rating.py
│   ├── migrations
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── *
│   ├── models
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── rating.py
│   │   ├── review.py
│   │   └── user.py
│   ├── routers
│   │   ├── category.py
│   │   ├── permission.py
│   │   ├── products.py
│   │   └── review.py
│   └── schemas
│       ├── category.py
│       ├── product.py
│       ├── review.py
│       └── user.py
├── README.md
├── pyproject.toml
└── uv.lock
```

### Порядок запуска

- Билд и запуск контейнеров ```docker-compose up -d --build```
- Миграция БД ```docker-compose exec web alembic upgrade head```


## TODO:
### Добавить информативное логирование приложения
При этом вынести модуль логирование в отдельный файл