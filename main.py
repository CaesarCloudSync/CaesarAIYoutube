import os
import io
import json
import base64
import hashlib
import asyncio 
import uvicorn
from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union,Optional
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from CaesarAIYoutube import CaesarAIYoutube
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


caesaryoutube = CaesarAIYoutube()
JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]
table = "caesaraiworldmodels"


@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIWorld!"
@app.get('/getaudio')# GET # allow all origins all methods.
async def getaudio(url:str):
    audio_stream = io.BytesIO()
    audio = caesaryoutube.get_audio(url)
    if audio:
        title = caesaryoutube.clean_filename(audio.title)
        audio_filename = f"{title}.mp3"
        audio.stream_to_buffer(audio_stream)
        audio_stream.seek(0)
        public_url = caesaryoutube.upload_to_bucket(audio_stream,audio_filename)
        return {"title":audio_filename,"video":public_url}
        

    else:
        return {"error":"no audio version exists"}

@app.get('/getvideo')# GET # allow all origins all methods.
async def getvideo(url:str):
    video_stream = io.BytesIO()
    video = caesaryoutube.get_video(url)
    if video:
        title = caesaryoutube.clean_filename(video.title)
        video_filename = f"{title}.mp4"
        video.stream_to_buffer(video_stream)
        video_stream.seek(0)
        public_url = caesaryoutube.upload_to_bucket(video_stream,video_filename)
        return {"title":video_filename,"video":public_url}

    else:
        return {"error":"no video version exists."}
@app.get('/getallmedia')# GET # allow all origins all methods.
async def getallmedia():
    
    return caesaryoutube.get_all_media()

@app.get('/searchfeed')# GET # allow all origins all methods.
async def searchfeed(query:str,amount : Optional[int] = 10):
    try:
        result = caesaryoutube.searchfeed(query=query,amount=amount)
        return result
    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}
@app.get('/playlistsearchfeed')# GET # allow all origins all methods.
async def playlistsearchfeed(query:str,amount : Optional[int] = 10):
    try:
        result = caesaryoutube.playlistsearchfeed(query=query,amount=amount)
        return result
    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}

@app.get('/getplaylistvideos')# GET # allow all origins all methods.
async def getplaylistvideos(url:str):
    try:
        result = caesaryoutube.get_playlist_videos(url)
        return result
    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}

@app.post("/deleteallmedia")
def deleteallmedia(data: JSONStructure = None):
    caesaryoutube.delete_all_media()
    return {"message":"all media was deleted."}


if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())