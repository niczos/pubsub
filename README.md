# PubSub GCP

## Usage 

#### Required: Python 3.9

To install client libraries use this command:
```python
pip install --upgrade google-cloud-pubsub
```

To install neccesary dependencies run command:
```python
pip install -r requirements.
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


