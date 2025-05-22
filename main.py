from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict
from RoleplayChat import RoleplayChat
from SpeechToText import SpeechToText
from TextToSpeech import AzureTextToSpeechProcessor
import os
from dotenv import load_dotenv
import io

# Carrega variáveis do .env
load_dotenv()

# Inicializa FastAPI
app = FastAPI()   # uvicorn main:app --reload

# Libera CORS para o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MODELOS ===

class StartRequest(BaseModel):
    prompt_name: str
    user_name: str
    user_description: str

class MessageRequest(BaseModel):
    user_message: str

class TextToSpeechRequest(BaseModel):
    text: str
    voice: str

# === ROLEPLAY ===

roleplay = None

@app.post("/api/start")
async def start_roleplay(data: StartRequest):
    global roleplay
    roleplay = RoleplayChat(data.prompt_name, data.user_name, data.user_description)
    return { "status": "iniciado", "mensagem_inicial": roleplay.history[-1]['content'] }
    #return { "status": "iniciado"}

@app.post("/api/roleplay")
async def continue_roleplay(data: MessageRequest):
    global roleplay
    if not roleplay:
        return { "erro": "Roleplay não iniciado. Use /api/start primeiro." }

    reply = roleplay.send_message(data.user_message)
    return { "reply": reply }

# === SPEECH TO TEXT ===

@app.post("/api/speech-to-text")
async def audio_to_text(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        transcription = SpeechToText.transcribe_audio(audio_bytes)
        return { "transcription": transcription }
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

# === TEXT TO SPEECH ===

@app.post("/api/text-to-speech")
async def text_to_audio(data: TextToSpeechRequest):
    try:
        processor = AzureTextToSpeechProcessor(text=data.text, voice=data.voice)
        audio_bytes = processor.synthesize_speech()

        return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/mpeg")
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})
