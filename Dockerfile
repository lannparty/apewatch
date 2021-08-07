FROM docker.io/library/python:3.9-slim AS requirements
WORKDIR /tmp

RUN pip install --no-cache-dir poetry
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry export > requirements.txt


FROM docker.io/library/python:3.9-slim AS build-image
WORKDIR /usr/src/app

COPY --from=requirements /tmp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY no_brakes ./no_brakes/

RUN groupadd -r rogue && useradd -r -g rogue rogue
USER rogue
ENV PYTHONPATH=/usr/src/app
ENTRYPOINT [ "python" ]