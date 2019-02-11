FROM python:3.7-alpine

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
  pipenv install psycopg2-binary && \
  apk --purge del .build-deps

RUN pipenv install

# Copy in source code
ADD ./manage.py .
ADD ./confero ./confero

# The web server will run on this port
EXPOSE 8000

ENTRYPOINT ["pipenv", "run", "python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]