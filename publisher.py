import os
from google.cloud import pubsub_v1

#topic_path = 'projects/rational-moon-320316/topics/pubsub1' 
topic_path = '<PATH_TO_TOPIC>' 
#credentials_path = '/Users/nika.jurczuk/pubsub/pubsub_key.json' #path to key file
credentials_path = '<PATH_TO_KEY>'

try:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
except NameError:
    print('Variable does not exist')

publisher = pubsub_v1.PublisherClient()

data = 'Hey Hi Hello!'
data = data.encode('utf-8')

future = publisher.publish(topic_path,data) #message id
print(f'published message id {future.result()}')