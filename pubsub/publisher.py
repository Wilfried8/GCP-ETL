import time

from google.cloud import pubsub_v1
import os
import sys

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project=os.environ['project_id'], topic=os.environ['topic_id'])

from datetime import datetime
import uuid

def get_data():
    import requests

    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]

    return res

def format_data(res):
    data = {}
    location = res['location']
    data['id'] = str(uuid.uuid4())
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def stream_data():
    import json
    import logging

    current_time = time.time()

    while True:
        if time.time() > current_time + 60:
            break
        try:
            res = get_data()
            res = format_data(res=res)

            json_data = json.dumps(res)
            bytes_data = json_data.encode("utf-8")

            future = publisher.publish(topic_path, bytes_data)
        except Exception as e:
            logging.error(f"An error occured : {e}")
            continue

stream_data()
print(f"Published messages to {topic_path}.")



g = get_data()
f = format_data(g)

#print(f)

#print(sys.argv[1])
#print(os.environ['region'])
