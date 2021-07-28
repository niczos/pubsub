import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

credentials_path = '/Users/nika.jurczuk/pubsub/pubsub_key.json' #path to key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/rational-moon-320316/subscriptions/pubsub1_sub'

def callback(message):
    print(f'Received message: {message}')
    print(f'data: {message.data}')
    message.ack() #delete message from servers

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'listening for message on {subscription_path}')

with subscriber:
    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
