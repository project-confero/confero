#! /bin/sh

# TODO: This only works on Linux
sudo -u postgres pg_dump -d confero -T fec_contribution > ./data/confero.sql  
