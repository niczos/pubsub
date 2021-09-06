# Copyright 2021 by Google.
# Your use of any copyrighted material and any warranties, if applicable, are subject to your agreement with Google.

import os
import logging
import re
import pytz 
import json
import googleapiclient.discovery
from google.oauth2 import service_account
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from logging.handlers import SysLogHandler

SCOPES = ['https://www.googleapis.com/auth/compute']
PROJECT_ID = '<PROJECT_ID>'
REGION = '<REGION>'

credentials_path = '<PATH_TO_KEY>'
subscription_path = '<PATH_TO_SUBSCRIPTION>'

MESSAGES = []

try:
    # set environmental variable
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    os.environ['GOOGLE_SUBSCRIPTION_PATH'] = subscription_path
except NameError:
    print('Variable does not exist')

timeout = 5

try:
    subscriber = pubsub_v1.SubscriberClient()
except ConnectionError:
    print("Can't connect to server.")


def callback(message):
    logging.info(message)
    MESSAGES.append(message.data)
    message.ack()  # delete message from servers
    #print(MESSAGES)

#################################################################
#                       smarts/netcool                          #
#################################################################

def filter_AND_SEND_messages(MESSAGE):

            #Regular expressions
            RESOURCE = re.search("(resource_display_name)(\W*)([a-zA-Z0-9-\s]*)", MESSAGE)
            EVENT_NAME = re.search("(policy_name)(\W*)([a-zA-Z0-9-\s]*)", MESSAGE)
            EVENT_SUMMARY = re.search("(condition_name)(\W*)([a-zA-Z0-9-\s]*)", MESSAGE)
            ROUTER_ID = re.search("(router_id)(\W*)([a-zA-Z0-9-\s./_?=-]*)", MESSAGE)

            name = re.search("(\"name\")(\W*)([a-zA-Z0-9-\s/]*)", MESSAGE)
            metric_type = re.search("(metric.type)(\W*)([a-zA-Z0-9-\s./_]*)", MESSAGE)
            resource_type = re.search("(resource.type)(\W*)([a-zA-Z0-9-\s./_]*)", MESSAGE)
            alignment_period = re.search("(alignmentPeriod)(\W*)([a-z{{A-Z0-9-\ns./_]*)", MESSAGE)
            per_series_aligner = re.search("(perSeriesAligner)(\W*)([a-z{{A-Z0-9-\ns./_]*)", MESSAGE)
            EVENT_TEXT ="name: "+  name.group(3), "displayName: "+  RESOURCE.group(3), "conditionThreshold : filter: metric type: "+ metric_type.group(3), "resource_type: " + resource_type.group(3), "aggregations: alignmentPeriod: " + alignment_period.group(3), "PerSeriesAligner: " + per_series_aligner.group(3)
            
            router_id = ROUTER_ID.group(3)
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path, scopes=SCOPES)
            compute = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
            response = compute.routers().list(project=f'{PROJECT_ID}', region=f'{REGION}', filter=(f"id={router_id}")).execute()

            if 'items' in response:
                for i in response['items']:
                   ROUTER_NAME = i['name']
            else:
                ROUTER_NAME = "None"
           
            SMARTS = "/opt/InCharge9/SAM/smarts/bin/sm_ems"
            SAM_BROKER = "loncdc11nmh30.uk.db.com:426"
            SAM_MANAGER = "London-EMEA"
            APP_NAME = "GCPMonitor"
            SOURCE = APP_NAME
            SEVERITY = 1

            print("OUTPUT=" ,  SMARTS, "-b",  SAM_BROKER, "-s", SAM_MANAGER, "-t", RESOURCE.group(3), "--create-system notify" , APP_NAME, RESOURCE.group(3), EVENT_NAME.group(3), SOURCE, "momentary 172800 severiy=", SEVERITY, "eventtext", EVENT_TEXT, "clearonacknowledge=TRUE category=Performanceuserdefined1=Core userdefined2=Script userdefined3=Prod userdefined12" , EVENT_SUMMARY.group(3), "2>&1", "Router_name: " +ROUTER_NAME)

def send_to_smarts(MESSAGES):
	for i in MESSAGES:
		MESSAGE_DECODED = i.decode()
		filter_AND_SEND_messages(MESSAGE_DECODED)

#################################################################
#                           GCP PART 2                          #
#################################################################

logger = logging.getLogger()
# change IP to your own public IP of the vm
logger.addHandler(SysLogHandler(address=('34.140.96.51', 514)))

streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback)
print(f'listening for message on {subscription_path}')

with subscriber:
    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # trigger the shutdown
        streaming_pull_future.result()  # block until shutdown is complete

send_to_smarts(MESSAGES)
