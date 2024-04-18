FROM python:3.11

WORKDIR /app

COPY poetry.lock* pyproject.toml ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
ENV PATH="$PATH:$POETRY_HOME/bin"


COPY . .

RUN ls -1a ./app
RUN poetry install --no-root --no-interaction

EXPOSE 1337

CMD ["python", "main.py"]
