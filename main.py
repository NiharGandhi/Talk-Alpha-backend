# uvicorn main:app
# uvicorn main:app --reload

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

from functions.database import store_message, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech


app = FastAPI()

origins = {
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "conversation_reset"}

@app.post("/post-audio-get/")
async def post_audio(file: UploadFile = File(...)):

    # audio_input = open(r"C:\Users\nihar\Desktop\Shawn\webapp\backend\voice.mp3", "rb")

    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    audio_input = open(file.filename, "rb")

    message_decode = convert_audio_to_text(audio_input)
    # print(message_decode)

    if not message_decode:
        return HTTPException(status_code=400, detail="FAILED TO DECODE AUDIO")
    
    # GPT RESOPNSE
    chat_response = get_chat_response(message_decode)

    if not chat_response:
        return HTTPException(status_code=400, detail="FAILED TO GET CHAT RESPONSE")

    store_message(message_decode, chat_response)
    print(chat_response)

    audio_output = convert_text_to_speech(chat_response)

    if not audio_output:
        return HTTPException(status_code=400, detail="FAILED TO GET ELEVEN LABS RESPONSE")
    
    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="application/octet-stream")

