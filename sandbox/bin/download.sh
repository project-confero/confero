#!/bin/sh

# Download
wget -P ./data/ https://www.fec.gov/files/bulk-downloads/2020/cn20.zip
wget -P ./data/ https://www.fec.gov/files/bulk-downloads/2020/ccl20.zip
wget -P ./data/ https://www.fec.gov/files/bulk-downloads/2020/indiv20.zip

# Unzip
unzip data/cn20.zip -d data
unzip data/ccl20.zip -d data
unzip data/indiv20.zip -d data
