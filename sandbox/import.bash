#!/bin/bash

# Create DB
psql -d confero_sandbox < ./sql/db.sql

# Candidates
xsv select -d "|" "CAND_ID,CAND_NAME,CAND_PTY_AFFILIATION,CAND_OFFICE,CAND_OFFICE_ST,CAND_OFFICE_DISTRICT" candidates.txt > candidates.csv
sed -i backup "1s/.*/id,name,party,office,state,district/" candidates.csv
psql -d confero_sandbox -c "COPY candidate (id,name,party,office,state,district) FROM '"$PWD/candidates.csv"' delimiter ',' csv header;"

# Committees
xsv select -d "|" "CAND_ID,CMTE_ID" committees.txt  > committees.csv
sed -i backup "1s/.*/candidate_id,committee_id/" committees.csv
sort -u committees.csv > committees.csv
psql -d confero_sandbox -c "COPY committee (candidate_id,committee_id) FROM '"$PWD/committees.csv"' delimiter ',' csv header;"

# Contributions
xsv select -d "|" "CMTE_ID,NAME,ZIP_CODE,EMPLOYER,OCCUPATION,SUB_ID" contributions.txt > contributions.csv
sed -i backup "1s/.*/committee_id,name,zip,employer,occupation,id/" contributions.csv
psql -d confero_sandbox -c "COPY contribution (committee_id,name,zip,employer,occupation,id) FROM '"$PWD/contributions.csv"' delimiter ',' csv header;"
