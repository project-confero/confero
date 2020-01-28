#!/bin/sh

# Download
wget -P ./sandbox/data/ https://www.fec.gov/files/bulk-downloads/2000/cn00.zip
wget -P ./sandbox/data/ https://www.fec.gov/files/bulk-downloads/2000/ccl00.zip
wget -P ./sandbox/data/ https://www.fec.gov/files/bulk-downloads/2000/indiv00.zip

# Unzip
unzip sandbox/data/cn00.zip -d ./sandbox/data
unzip sandbox/data/ccl00.zip -d ./sandbox/data
unzip sandbox/data/indiv00.zip -d ./sandbox/data
