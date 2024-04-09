# GCP-ETL

pour se loger
gcloud auth application-default login 

pour changer de projet:
gcloud config set project gcp-etl-419719

change service account :
export GOOGLE_CREDENTIALS="/Users/tayo/Documents/DataEngineer/GCP-ETL/keys/gcp-etl-419719-7b35ff57c8c5.json" 
GCP-ETL git:(main) ✗ gcloud auth activate-service-account --key-file=/Users/tayo/Documents/DataEngineer/GCP-ETL/keys/gcp-etl-419719-7b35ff57c8c5.json --project=gcp-etl-419719

chmod +x venv.sh : pour donner les permissions pur l'exécution du script 
source venv.sh

gcloud pubsub subscriptions **create** sub-profile-api --topic=$topic_id : create subcription

**pubsubtogcs**
python3 pubsub/PubSubToGcs.py \
  --project=$project_id \
  --input_topic=projects/$project_id/topics/$topic_id \
  --output_path=gs://$bucket_name_api/samples/output \
  --runner=DataflowRunner \
  --window_size=1 \
  --temp_location=gs://$bucket_name_api/temp

**gcstobq**
python3 dataflow/GcsToBq.py \
  --project=$project_id \
  --input_bucket=$bucket_name_faker
  --input_file=dataset_10000.parquet
  --output_table=$bq_dataset_name.$bq_table_name
  --runner=DataflowRunner \
  --temp_location=gs://$bucket_name_faker/temp