#! /bin/sh

# TODO: This only works on Linux
sudo -u postgres pg_dump -Fc -d confero -T fec_contribution > ./data/confero_archive
