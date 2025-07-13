FROM python:3.12

WORKDIR /app

COPY pyproject.toml .
RUN pip install poetry && poetry install

COPY ./app ./app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
