import os
import io
import json
import base64
import hashlib
import asyncio 
import uvicorn
from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form, Query
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union,Optional
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from CaesarAIYoutube import CaesarAIYoutube
from CaesarAIGCP.CaesarAIGCP import CaesarAIGCP
from google.cloud import storage
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

caesaraigcp = CaesarAIGCP()
bucket_name = "caesaraiyoutube-bucket"
caesaryoutube = CaesarAIYoutube()
JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]
table = "caesaraiworldmodels"


@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIWorld!"
@app.get('/getaudiodownload')# GET # allow all origins all methods.
async def getaudiodownload(url:str):
    audio = caesaryoutube.get_audio(url)
    if audio:
        title = caesaryoutube.clean_filename(audio.title)
        video_filename = f"{title}.mp3"
        bucket_exists = caesaraigcp.blob_exists(bucket_name,video_filename)
        if not bucket_exists:
            
            filesize = audio.filesize
            return StreamingResponse(caesaryoutube.stream_to_bucket(audio.url,filesize,video_filename),status_code=status.HTTP_200_OK,
                                    media_type='text/event-stream') #Response(buffer.getvalue(), headers=headers, media_type='video/mp4')
        else:
            return f"https://storage.googleapis.com/{bucket_name}/{video_filename}"

    else:
        return {"error":"no video version exists."}

@app.get('/getaudiowatch')# GET # allow all origins all methods.
async def getaudiowatch(url: str = Query(..., description="The YouTube video URL to extract audio from")):
    audio = caesaryoutube.get_audio(url)
    if audio:
        title = caesaryoutube.clean_filename(audio.title)
        video_filename = f"{title}.mp3"
        return {"title":video_filename,"media":audio.url}

    else:
        return {"error":"no video version exists."}

@app.get('/getvideowatch')# GET # allow all origins all methods.
async def getvideowatch(url:str):
    
    video = caesaryoutube.get_video(url)
    
    if video:
        title = caesaryoutube.clean_filename(video.title)
        video_filename = f"{title}.mp4"
        return {"title":video_filename,"media":video.url}

    else:
        return {"error":"no video version exists."}
    
@app.get('/getvideodownload')# GET # allow all origins all methods.
async def getvideodownload(url:str):
    
    video = caesaryoutube.get_video(url)
    
    if video:
        title = caesaryoutube.clean_filename(video.title)
        video_filename = f"{title}.mp4"
        bucket_exists = caesaraigcp.blob_exists(bucket_name,video_filename)
        if not bucket_exists:
            
            filesize = video.filesize
            return StreamingResponse(caesaryoutube.stream_to_bucket(video.url,filesize,video_filename),status_code=status.HTTP_200_OK,
                                    media_type='text/event-stream') #Response(buffer.getvalue(), headers=headers, media_type='video/mp4')
        else:
            return f"https://storage.googleapis.com/{bucket_name}/{video_filename}"

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
@app.delete("/deletemedia")
def deletemedia(blob_name:str,bucket_name : Optional[str] = "caesaraiyoutube-bucket"):
    caesaraigcp.delete_blob(blob_name,bucket_name)
    return {"message":"media deleted."}

@app.post("/deleteallmedia")
def deleteallmedia(data: JSONStructure = None):
    return StreamingResponse(caesaraigcp.delete_all_media(),status_code=status.HTTP_200_OK,
                        media_type='text/event-stream') #Response(buffer.getvalue(), headers=headers, media_type='video/mp4')



if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())