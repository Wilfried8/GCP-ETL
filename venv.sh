#!/bin/zsh

export project_id=gcp-etl-419719
export region=EUROPE-WEST9
export topic_id=profile-api
export bucket_name_api=profile-api
export bucket_name_faker=profile-faker
export bq_dataset_name=dataset1_gcp_etl
export bq_table_name=table1_gcp_etl


#print variable

echo -e "\nYour environment variables have been initialised as follows:"
echo -e "\t\project_id:"  $project_id
echo -e "\t\region:"  $region
echo -e "\t\topic_id:"  $topic_id
echo -e "\t\bucket_name_api:"  $bucket_name_api
echo -e "\t\bucket_name_faker:"  $bucket_name_faker
echo -e "\t\bq_dataset_name:"  $bq_dataset_name
echo -e "\t\bq_table_name:"  $bq_table_name
