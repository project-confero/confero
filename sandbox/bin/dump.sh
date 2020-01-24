#! /bin/sh

# TODO: This only works on Linux
sudo -u postgres pg_dump -Fc --no-acl --no-owner -d confero > ./sandbox/data/confero.dump
