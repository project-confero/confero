# Confero

Tracking FEC Contribution Data

## Local Development

Docker is nice for deploying, CI, and debugging issues in those two environments. But it can be a pain for local development.
And if you're using docker to run the server locally, you'll want a local environment for your editor and quality checkers. So let's set that up first.

### Prerequisites

Install [Python 3.7](https://www.python.org/downloads/)

Also, for some formatter tooling, install [Node](https://nodejs.org/en/download)

You'll also need prettier for formatting:

```bash
npm install -g prettier
```

### Setup

Install and use pipenv:

Install pipenv

```bash
brew install pipenv
```

or

```bash
pip install --user pipenv
```

Then setup the virtual env and install dependencies.

```bash
pipenv install --dev
```

Then enter the virtual env

```bash
pipenv shell
```

### Run Server

```bash
pipenv shell
python manage.py runserver
```

## Adding Dependencies

```bash
pipenv install NAME
pipenv install NAME --dev # for non-production dependencies
```

## Local Docker

You can use Docker to run the project in the same environment it'll
be in for production. This is particularly useful for debugging weird production errors.

To help with that, we're using [docker-compose](https://docs.docker.com/compose/), which allows you to spin up the whole project, with a database, in a single command.

### Prerequisites

Install Docker and docker-compose:

```bash
brew cask install docker
```

Or see the docs for
[Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
or [Windows](https://docs.docker.com/docker-for-windows/install/).

### Setup

This will build the docker containers needed to run the app.

```bash
docker-compose build
```

### Run Server

Starts up the docker-compose cluster, and runs the app on localhost:8000.

```bash
docker-compose up
```

### Run a manage.py command

```bash
docker-compose run django COMMAND

# Example: run migrations:
docker-compose run django migrate
```

### Run a system command

`docker-compose run django` passes commands to the `python manage.py` entrypoint by default.
To override that:

```bash
docker-compose run --entrypoint COMMAND django
```

## Code Quality

We're using tests, linters, and formatters to make sure everything is working as it should.

All these things will run in CI, and will have to pass before you can merge and deploy code.

To run all the quality checks locally and ensure CI will pass, run:

```bash
./bin/quality
```

### Testing

See the [Django Docs](https://docs.djangoproject.com/en/2.1/topics/testing/overview/) for info on writing tests.

#### Run all tests

```bash
./bin/test
```

#### Get a code coverage report

This will run all the tests, and then report on which lines of code are uncovered by tests.

After running `./bin/coverage`, you can see a detailed report by opening
`./htmlcov/index.html` in your browser.

```bash
./bin/coverage
```

#### Run all tests from within docker

If tests are failing in CI, running the tests in docker could help figure out what's up.

_Warning_: Running docker-compose commands may not work from within a virtualenv.

```bash
./bin/docker-test
```

or

```bash
./bin/docker-coverage
```

### Linting/Formatting

Worrying about code style is lame, so let's make robots do it for us.

We're using a few code quality tools:

- [yapf](https://github.com/google/yapf) - Google auto-formatter
- [prospector](https://github.com/PyCQA/prospector) - Runs a bunch of linters with reasonable defaults
- [prettier](https://github.com/prettier/prettier) - A JavaScript formatter. Just used for .md files for this project.
- [`pre-commit`](https://pre-commit.com) - run the quality checks on every commit

#### Pre-Commit Hook

When you're committing, the pre-commit hook will run the linter and formatters on all the staged files. If anything fails, the hook will fail.

Note that if the yapf formatter fixes anything, that will cause the hook to fail. Check that the changes look good, then apply the commit again to see it pass.

To set up the pre-commit hook:

```bash
pre-commit install
```

Note that once this is set up, you'll get an error if you try to commit outside of your virtualenv.

#### Run All

To run the quality checks on the whole project:

```bash
./bin/lint
```

#### Auto-format

If you just want to auto-format the project, run:

```bash
./bin/format
```
