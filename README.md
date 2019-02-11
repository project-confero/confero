# Confero

Tracking FEC Contribution Data

## Development

### Setup

Install Python 3.7

Then install and use pipenv:

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

While you'll want a local environment for your editor and quality checkers,
you can use Docker to run the project in the same environment it'll
be in for production.

We're also using [docker-compose](https://docs.docker.com/compose/), which allows you to spin up the whole project, with a database, in a single command.

#### Prerequisites

Install Docker and docker-compose:

```bash
brew cask install docker
```

Or see the docs for
[Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
or [Windows](https://docs.docker.com/docker-for-windows/install/).

### Setup

```bash
docker-compose build
```

### Run Server

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

#### Run all tests from within docker

```bash
./bin/docker-test
```

#### Get a code coverage report

```bash
./bin/docker-coverage
```

After running `./bin/coverage`, you can see a detailed report by opening
`./htmlcov/index.html` in your browser.

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

#### Run All

To run the quality checks on the whole project:

```bash
pre-commit run --all-files
```

#### Auto-format

If you just want to auto-format the project, run:

```bash
./bin/format
```
