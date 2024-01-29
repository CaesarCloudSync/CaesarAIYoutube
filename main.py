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
    audio = caesaryoutube.get_audio(url)
    if audio:
        title = caesaryoutube.clean_filename(audio.title)
        headers = {'Content-Disposition': f'inline; filename="{title}.mp3"'} # ,"Content-length":str(audio.filesize)
        return StreamingResponse(caesaryoutube.stream_media(audio.url),headers=headers,status_code=status.HTTP_200_OK,
                                media_type="audio/mpeg") #Response(buffer.getvalue(), headers=headers, media_type='video/mp4')
    else:
        return {"error":"no audio version exists"}

@app.get('/getvideo')# GET # allow all origins all methods.
async def getvideo(url:str):
    video = caesaryoutube.get_video(url)
    if video:
        title = caesaryoutube.clean_filename(video.title)
        headers = {'Content-Disposition': f'inline; filename="{title}.mp4'} #,"Content-length":str(video.filesize)
        return StreamingResponse(caesaryoutube.stream_media(video.url),headers=headers,status_code=status.HTTP_200_OK,
                                media_type="video/mp4") #Response(buffer.getvalue(), headers=headers, media_type='video/mp4')
    else:
        return {"error":"no video version exists."}
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



if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())