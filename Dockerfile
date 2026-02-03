FROM python:3.13-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN pip install "poetry==1.8.3"

RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

COPY --chown=app:app poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    && poetry install --only=main --no-root

COPY --chown=app:app src/ ./

ENV PATH="/home/app/.venv/bin:$PATH"
EXPOSE 8080

CMD ["python", "main.py"]
