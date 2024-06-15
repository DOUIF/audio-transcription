FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y ffmpeg

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY . /app/

EXPOSE 5001

CMD ["fastapi", "run", "main.py", "--port", "5001"]
