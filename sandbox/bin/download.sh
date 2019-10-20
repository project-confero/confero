#!/bin/sh

# Download
wget https://www.fec.gov/files/bulk-downloads/2020/cn20.zip data/
wget https://www.fec.gov/files/bulk-downloads/2020/ccl20.zip data/
wget https://www.fec.gov/files/bulk-downloads/2020/indiv20.zip data/

# Unzip
unzip data/cn20.zip -d data
unzip data/ccl20.zip -d data
unzip data/indiv20.zip -d data
