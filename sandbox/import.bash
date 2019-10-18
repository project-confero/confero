#!/bin/bash

# Create DB
psql confero_sandbox < ./sql/db.sql

# Candidates
xsv select -d "|" "CAND_ID,CAND_NAME,CAND_PTY_AFFILIATION,CAND_OFFICE" candidates.txt > candidates.csv
sed -i csv "1s/.*/id,candidate_name,party,candidate_office/" candidates.csv
psql -c "COPY candidates FROM './candidates.csv' delimiter '|' csv headers;"

# Committees
xsv select "CAND_ID,CMTE_ID,LINKAGE_ID" committees.txt  > committees.csv
sed -i csv "1s/.*/candidate_id,committee_id,linkage_id/" committees.csv
sort -u committees.csv > committees.csv
psql -c "COPY committee FROM './committees.csv' delimiter '|' csv headers;"

# Contributions
xsv select -d "|" "CMTE_ID,NAME,ZIP_CODE,SUB_ID" itcont_2020_20190629_20190930.txt > contributions.csv
sed -i csv "1s/.*/committee_id,contributor_name,zip,id/" contributions.csv
psql -c "COPY contributions FROM './contributions.csv' delimiter '|' csv headers;"

# Download tables for graphing and 