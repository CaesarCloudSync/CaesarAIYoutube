import re
from pytube import YouTube,request
from youtubesearchpython import VideosSearch,PlaylistsSearch,Playlist


class CaesarAIYoutube:
    def __init__(self) -> None:
        pass

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
#cy = CaesarAIYoutube()
#
#cy.searchfeed("2024 playboi carti")


