FROM python:3.7-slim-buster AS base

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

# The web server will run on this port
EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]

# Dev setup. For running tests and other dev tools.
FROM base AS dev

RUN pipenv install --dev --system

# Copy in tools
ADD ./.coveragerc .
ADD ./bin ./bin

# Copy in all source code
ADD ./ .


# Prod. Do this last, so by default dev dependencies are ignored.
FROM base AS prod

RUN pipenv install --system

# Copy in source code
ADD ./manage.py .
ADD ./confero ./confero
ADD ./fec ./fec
