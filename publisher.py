import os
from google.cloud import pubsub_v1

credentials_path = '/home/nika_jurczuk//pubsub_key.json'
#credentials_path = '<PATH_TO_KEY>'
topic_path = 'projects/rational-moon-320316/topics/demo-topic'
#topic_path = '<PATH_TO_TOPIC>'

try:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    os.environ['GOOGLE_TOPIC_PATH'] = topic_path
except NameError:
    print('Variable does not exist')

publisher = pubsub_v1.PublisherClient()

for i in range(10):
    data = str(i)
    data = data.encode('utf-8')
    future = publisher.publish(topic_path, data)  # message id

print(f'published message id {future.result()}')
