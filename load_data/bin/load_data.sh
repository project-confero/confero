python bq_to_gcs.py --sql sql/connections.sql \
 --year '20' \
 --output gs://$BUCKET/test/test.json \
 --project $PROJECT \
 --job_name bqtogcs \
 --staging_location gs://$BUCKET/staging \
 --temp_location gs://$BUCKET/temp \
 --region us-west2 \
 --runner DataflowRunner
