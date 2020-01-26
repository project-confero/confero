#!/bin/sh

# Download
wget -P ./sandbox/data/ https://www.fec.gov/files/bulk-downloads/2020/cn20.zip
wget -P ./sandbox/data/ https://www.fec.gov/files/bulk-downloads/2020/ccl20.zip
wget -P ./sandbox/data/ https://www.fec.gov/files/bulk-downloads/2020/indiv20.zip

# Unzip
unzip sandbox/data/cn20.zip -d data
unzip sandbox/data/ccl20.zip -d data
unzip sandbox/data/indiv20.zip -d data
