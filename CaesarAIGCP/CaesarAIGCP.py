import os
import json
import base64
from google.cloud import storage
class CaesarAIGCP:
    def __init__(self) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(f"{dir_path}/creds.txt") as f:
            service_base64 = f.read()
        service_info = json.loads(base64.b64decode(service_base64.encode()).decode())
        self._client = storage.Client.from_service_account_info(service_info)

    def make_blob_public(self,blob_name,bucket_name:str="caesaraiyoutube-bucket"):
        """Makes a blob publicly accessible."""
        # bucket_name = "your-bucket-name"
        # blob_name = "your-object-name"
        bucket = self._client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.make_public()

        #print(
        #    f"Blob {blob.name} is publicly accessible at {blob.public_url}"
        #)
    def blob_exists(self,bucket_name, filename):
        bucket = self._client.get_bucket(bucket_name)
        blob = bucket.blob(filename)
        return blob.exists()
    def upload_to_bucket(self,  file_bytes,blob_name:str,bucket_name:str="caesaraiyoutube-bucket"):
        """ Upload data to a bucket"""
        
        # Explicitly use service account credentials by specifying the private key
        # file.


        #print(buckets = list(client.list_buckets())
        bucket = self._client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_file(file_bytes) #upload_from_filename(path_to_file)
        
        #returns a public url
        self.make_blob_public(blob_name,bucket_name)
        return blob.public_url
    def get_all_media(self,bucket_name:str="caesaraiyoutube-bucket"):
        bucket =self._client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()
        return [{"title":blob.name,"url":blob.media_link}for blob in blobs]


    def delete_all_media(self,bucket_name:str="caesaraiyoutube-bucket"):
        bucket =self._client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()
   
        for ind,blob in enumerate(blobs):
            #print(blob)
            blob.delete()
            yield f"{ind}:{blob.name}\n"
    def delete_blob(self,blob_name:str,bucket_name:str="caesaraiyoutube-bucket"):
        bucket =self._client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()


