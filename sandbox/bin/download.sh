#!/bin/bash

year=$1
yr=${1: -2}

echo "downloading data for ${year} (${yr})"

# Download
wget -P ./sandbox/data/$year https://www.fec.gov/files/bulk-downloads/$year/cn${yr}.zip
wget -P ./sandbox/data/$year https://www.fec.gov/files/bulk-downloads/$year/ccl${yr}.zip
wget -P ./sandbox/data/$year https://www.fec.gov/files/bulk-downloads/$year/indiv${yr}.zip

# Unzip
unzip sandbox/data/$year/cn$yr.zip -d sandbox/data/$year
unzip sandbox/data/$year/ccl$yr.zip -d sandbox/data/$year
unzip sandbox/data/$year/indiv$yr.zip -d sandbox/data/$year
