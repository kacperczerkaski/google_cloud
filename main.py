from googleapiclient.discovery import build
import functions_framework
from google.cloud import storage   
apikey = ''
tservice = build("translate", "v2", developerKey =apikey )


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def hello_gcs(cloud_event):
    data = cloud_event.data
    event_id = cloud_event["id"]
    event_type = cloud_event["type"]
    bucket = data["bucket"]
    name = data["name"]
    typ_file = data["contentType"]
    
    if typ_file == 'text/plain':
      storage_client = storage.Client()
      bucket = storage_client.bucket(bucket)
      blob = bucket.blob(name)
      new_file = name[:-4] + '_PL.txt'
      blob_new = bucket.blob(new_file)

      with blob.open("r") as f:
        content = f.read()
        content_translate = tservice.translations().list(source ='en', target='pl', q = content).execute()
        trans = content_translate['translations'][0]['translatedText']
        
        with blob_new.open("w") as f:
          f.write(trans)