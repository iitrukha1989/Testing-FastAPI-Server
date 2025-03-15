FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update
RUN apt-get install libpq-dev -y

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

RUN uv pip freeze > requirements.txt 
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install --no-cache-dir uvicorn

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
