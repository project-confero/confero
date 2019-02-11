FROM python:3.7-alpine AS base

ENV PYTHONUNBUFFERED 1

ARG PROJECT=confero
ARG PROJECT_DIR=/code

# Set up container directory
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

# Install deps first, for caching
RUN pip install pipenv 
ADD ./Pipfile .
ADD ./Pipfile.lock .

# Install Postgres Backend
RUN \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
  # Actuall install dependencies, including psycopg2
  pipenv install --system && \
  apk --purge del .build-deps

# The web server will run on this port
EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]

# Dev setup. For running tests and other dev tools.
FROM base AS dev

RUN pipenv install --dev --system

ADD ./.coveragerc .
ADD ./bin ./bin

RUN mkdir /htmlcov

# Copy in source code
ADD ./manage.py .
ADD ./confero ./confero

# Prod. Do this last, so by default dev dependencies are ignored.
FROM base AS prod

# Copy in source code
ADD ./manage.py .
ADD ./confero ./confero