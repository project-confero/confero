# Confero

Tracking FEC Contribution Data

## Local Docker

### Prerequisites

Install Docker and docker-compose:

```bash
brew cask install docker
```

Or see the docs for
[Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
or [Windows](https://docs.docker.com/docker-for-windows/install/).

### Setup

```bash
docker build -t confero .
```

### Run Server

```bash
docker run -p 8000:8000 confero
```

## Development without Docker

### Setup

```bash
python -m virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### Run Server

```bash
python manage.py runserver
```

## Adding Dependencies

```bash
pip install dependency-name
pip freeze > requirements.txt
```

## Linting/Formatting

Worrying about code style is lame, so let's make robots do it for us.

We're using a few code quality tools:

- [yapf](https://github.com/google/yapf) - Google auto-formatter
- [prospector](https://github.com/PyCQA/prospector) - Runs a bunch of linters with reasonable defaults
- [prettier](https://github.com/prettier/prettier) - A JavaScript formatter. Just used for .md files for this project.
- [`pre-commit`](https://pre-commit.com) - run the quality checks on every commit

### Setup

To set up the pre-commit hook:

```bash
pre-commit install
```

### Run All

To run the quality checks on the whole project:

```bash
pre-commit run --all-files
```
