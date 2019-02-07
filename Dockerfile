FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

# TODO: Install build deps?
RUN apk add git
RUN apk add openssh

ARG PROJECT=confero
ARG PROJECT_DIR=/code

# Set up container directory
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

# Install deps first, for caching
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy in source code
ADD . ./

# The web server will run on this port
EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
