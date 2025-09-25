import re
import sys
from CaesarAIGCP.CaesarAIGCPStreamUpload import CaesarAIGCPStreamUpload
from pytube import YouTube,request
from youtubesearchpython import VideosSearch,PlaylistsSearch,Playlist

class CaesarAIYoutube:
    def __init__(self) -> None:
        pass
    def searchfeed(self,query:str,amount=10):
        print("hi")
        videosSearch = VideosSearch(query, limit =amount)
        print("hello")


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
        video.filesize
        if video:
            return video
        else:
            return None
    def get_playlist_videos(self,url):
        playlist = Playlist(url)
        return {"result":playlist.videos}
    def stream_to_bucket(self,mediaurl:str,filesize:str,blob_name:str,bucket_name:str="caesaraiyoutube-bucket"):
        with CaesarAIGCPStreamUpload(bucket_name=bucket_name, blob_name=blob_name)as gcp_upload_stream:
            for ind,chunk in enumerate(request.stream(mediaurl)):
                gcp_upload_stream.write(chunk)
                progress = ((ind * sys.getsizeof(chunk)/filesize) * 100)
                yield f"{progress:.2f}%\n"
        bucket = gcp_upload_stream._client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.make_public()
        yield f"https://storage.googleapis.com/{bucket_name}/{blob_name}"                


