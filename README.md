# PubSub GCP
The script gets the alerts from GCP router and send to pubsub, smarts and netcool.

## Usage 

#### Required: Python 3


To install neccesary dependencies run command:
```python
pip install -r requirements.txt
```
In files subcriber.py and publisher.py in fields subscription_path, credentials_path and topic_path set your own paths. Create key with service account and save it. To write to syslog you may have to run `chmod 775` (or change syslog.conf). You must have Admin Pubsub or Owner role to run it. 

In file terraform.tfvars set your own region and project ID.

Run command `terraform init` to initialize directory. Then run `terraform apply`.

To send message run 
```python
python subscriber.py
```

in command prompt and 
```python
python publisher.py
```
in other terminal.

### Smarts_script.py
Set your own variables: project_id, region, path to your json account service key and path to subscription in pubsub. Also change IP to your own public IP of the vm. 


