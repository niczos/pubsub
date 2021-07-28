import os
from google.cloud import pubsub_v1

credentials_path = '/Users/nika.jurczuk/pubsub/pubsub_key.json' #path to key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/rational-moon-320316/topics/pubsub1'

data = 'Hey Hi Hello!'
data = data.encode('utf-8')

future = publisher.publish(topic_path,data) #message id
print(f'published message id {future.result()}')