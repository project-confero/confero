#!/bin/sh
gsutil mb -p $PROJECT gs://$DATA_BUCKET/
gsutil mb -p $PROJECT -l $REGION gs://$BUCKET/
gsutil acl ch -g allUsers:R gs://$DATA_BUCKET/
gsutil cp nameParser.js gs://$BUCKET/project/nameParser.js
gsutil cp data/names.csv gs://$BUCKET/project/names.csv
