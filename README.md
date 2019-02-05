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
pip -r requirements.txt
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