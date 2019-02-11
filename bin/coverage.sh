#!/bin/sh

coverage run --source='.' manage.py test confero && \
coverage html && \
coverage report

