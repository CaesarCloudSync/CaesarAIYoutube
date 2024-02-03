import io
import re
import json
import base64
from google.cloud import storage
from pytube import YouTube,request
from youtubesearchpython import VideosSearch,PlaylistsSearch,Playlist


class CaesarAIYoutube:
    def __init__(self) -> None:
        with open("creds.txt") as f:
            service_base64 = f.read()
        service_info = json.loads(base64.b64decode(service_base64.encode()).decode())
        self.storage_client = storage.Client.from_service_account_info(service_info)

    def searchfeed(self,query:str,amount=10):
        videosSearch = VideosSearch(query, limit =amount)

        return videosSearch.result()
    def playlistsearchfeed(self,query:str,amount=10):
        videosSearch = PlaylistsSearch(query, limit =amount)

        return videosSearch.result()
        
    def stream_media(self,mediaurl):
        for chunk in request.stream(mediaurl):
            yield chunk
    def clean_filename(self,filename):
        return re.sub(r'[^\w_.)( -]', '', filename).replace('"',"",100)
    def get_audio(self,url):
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
        if audio:
            return audio
        else:
            return None
    def get_video(self,url):
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True).get_highest_resolution()
        if video:
            return video
        else:
            return None
    def get_playlist_videos(self,url):
        playlist = Playlist(url)
        return {"result":playlist.videos}
    def make_blob_public(self,blob_name,bucket_name:str="caesaraiyoutube-bucket"):
        """Makes a blob publicly accessible."""
        # bucket_name = "your-bucket-name"
        # blob_name = "your-object-name"
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.make_public()

        #print(
        #    f"Blob {blob.name} is publicly accessible at {blob.public_url}"
        #)

    def upload_to_bucket(self,  file_bytes,blob_name:str,bucket_name:str="caesaraiyoutube-bucket"):
        """ Upload data to a bucket"""
        
        # Explicitly use service account credentials by specifying the private key
        # file.


        #print(buckets = list(storage_client.list_buckets())
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
     
        blob.upload_from_file(file_bytes) #upload_from_filename(path_to_file)
        
        #returns a public url
        self.make_blob_public(blob_name,bucket_name)
        return blob.public_url
    def delete_all_media(self,bucket_name:str="caesaraiyoutube-bucket"):
        bucket =self.storage_client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()
        for blob in blobs:
            print(blob)
            blob.delete()


if __name__ == "__main__":
    pass
    #caesaryoutube = CaesarAIYoutube()
    

    #cy = CaesarAIYoutube()
    #with open("car.jpeg","rb") as f:
    #    cy.upload_to_bucket("caesaraiyoutube-bucket",f,"car.jpeg")
    #
    #cy.searchfeed("2024 playboi carti")


