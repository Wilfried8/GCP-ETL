# [START pubsub_to_gcs]
import argparse
from datetime import datetime
import logging
import random

from apache_beam import (
    DoFn,
    GroupByKey,
    io,
    ParDo,
    Pipeline,
    PTransform,
    WindowInto,
    WithKeys,
)
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions
from apache_beam.transforms.window import FixedWindows
from apache_beam.io import ReadFromParquet, WriteToBigQuery


class ProcessData(DoFn):
    def process(self, element):
        element.pop('text', None)
        element.pop('longitude', None)
        element.pop('latitude', None)
        element.pop('ip_address', None)
        element.pop('credit_card_number', None)
        element.pop('last_activity', None)
        element.pop('join_date', None)

        # text, longitude, latitude, city, country, ip_address, credit_card_number, last_activity, last_activity, join_date, birthdate, job_title, company
        return [element]

def run(input_bucket, input_file, output_table, pipeline_args=None):

    pipeline_options = PipelineOptions(
        pipeline_args
    )

    with Pipeline(options=pipeline_options) as pipeline:
        lines = pipeline | 'ReadFromGCS' >> ReadFromParquet(f'gs://{input_bucket}/{input_file}')
        processes_data = lines | 'ProcessData' >> ParDo(ProcessData())
        processes_data | 'WriteToBigquery' >> WriteToBigQuery(
            output_table,
            schema='id:STRING, name:STRING, email:STRING, phone_number:STRING, address:STRING, company:STRING, job_title:STRING, birthdate:DATE, country:STRING, city:STRING',
            write_disposition=io.BigQueryDisposition.WRITE_TRUNCATE,
            create_disposition=io.BigQueryDisposition.CREATE_IF_NEEDED
        )

if __name__=="__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_bucket",
        help="The input_bucket"
        '"projects/<PROJECT_ID>/topics/<TOPIC_ID>".',
    )
    parser.add_argument(
        "--input_file",
        help="Output file's window size in minutes.",
    )
    parser.add_argument(
        "--output_table",
        help="output_table in BQ",
    )

    known_args, pipeline_args = parser.parse_known_args()

    run(
        known_args.input_bucket,
        known_args.input_file,
        known_args.output_table,
        pipeline_args,
    )