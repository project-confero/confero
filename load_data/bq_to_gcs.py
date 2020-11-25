from __future__ import absolute_import

import json

import argparse
import logging

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

def run(argv=None):
    parser = argparse.ArgumentParser()

    # custom arguments for bigquery SQL and GCS output location
    parser.add_argument('--year',
                        dest='year',
                        help='year to load.')
    parser.add_argument('--sql',
                        dest='sql',
                        help='bigquery sql to extract req columns and rows.')
    parser.add_argument('--output',
                        dest='output',
                        help='gcs output location for json files.')
    known_args, pipeline_args = parser.parse_known_args(argv)
    options = PipelineOptions(pipeline_args)

    # instantiate a pipeline with all the pipeline option
    p = beam.Pipeline(options=options)
    with open(known_args.sql) as file:
        sql = file.read().format(year=known_args.year)

    # processing and structure of pipeline
    p \
    | 'Input: QueryTable' >> beam.io.Read(beam.io.BigQuerySource(
        query=sql,
        use_standard_sql=True)) \
    | 'FormatOutput' >> beam.Map(json.dumps) \
    | 'Output: Export to JSON' >> beam.io.WriteToText(known_args.output)

    result = p.run()
    result.wait_until_finish()  # Makes job to display all the logs

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
