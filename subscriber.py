import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from logging.handlers import SysLogHandler
import logging

credentials_path = '/home/nika_jurczuk/dataflow-pubsub-key.json'
# credentials_path = '<PATH_TO_KEY>'

subscription_path = 'projects/dataflow-poc-317213/subscriptions/demo-sub'
# subscription_path = '<PATH_TO_SUBSCRIPTION>'

logging.basicConfig(filename='/var/log/syslog', level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')

try:
    # set environmental variable
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    os.environ['GOOGLE_SUBSCRIPTION_PATH'] = subscription_path
except NameError:
    print('Variable does not exist')

# set timeout to 8s
timeout = 8

subscriber = pubsub_v1.SubscriberClient()


def callback(message):
    print(f'Received message: {message}')
    print(f'data: {message.data}')
    logging.info(message)
    with open('output.txt', 'a') as f:
        f.write(f'{message.data}')
        f.close()
    message.ack()  # delete message from servers


logger = logging.getLogger()
# change IP to your own public IP of the vm
logger.addHandler(SysLogHandler(address=('34.118.32.203', 514)))

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'listening for message on {subscription_path}')

logging.warning("Siema")

with subscriber:
    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError: #always go there after timeout
  #      with open('output.txt', 'w') as f:
   #         f.write('Loading failed due to Timeout')
    #        f.close()
        streaming_pull_future.cancel()  # trigger the shutdown
        streaming_pull_future.result()  # block until shutdown is complete
    
