#!/bin/sh
gcloud iam service-accounts create $USER_NAME
gcloud projects add-iam-policy-binding $PROJECT --member="serviceAccount:$USER_NAME@$PROJECT.iam.gserviceaccount.com" --role=roles/bigquery.jobUser
gcloud projects add-iam-policy-binding $PROJECT --member="serviceAccount:$USER_NAME@$PROJECT.iam.gserviceaccount.com" --role=roles/storage.objectViewer
gcloud projects add-iam-policy-binding $PROJECT --member="serviceAccount:$USER_NAME@$PROJECT.iam.gserviceaccount.com" --role=roles/bigquery.dataEditor
gcloud projects add-iam-policy-binding $PROJECT --member="serviceAccount:$USER_NAME@$PROJECT.iam.gserviceaccount.com" --role=roles/storage.objectCreator
gcloud iam service-accounts keys create $GOOGLE_APPLICATION_CREDENTIALS --iam-account="$USER_NAME@$PROJECT.iam.gserviceaccount.com"
