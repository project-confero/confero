FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

# Copy in dependencies
ADD requirements.txt /requirements.txt

# TODO: Install build deps?

# Set up container directory
RUN mkdir /code
WORKDIR /code

# Install deps first, for caching
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy in source code
ADD . /code/

# The web server will run on this port
EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
