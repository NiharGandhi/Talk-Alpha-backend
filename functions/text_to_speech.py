import requests

from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

def convert_text_to_speech(message):

    body= {
        "model_id": "eleven_monolingual_v1",
        "text": message,
        "voice_settings": {
            "similarity_boost": 0,
            "stability": 0
        }
    }

    voice_rachel = "21m00Tcm4TlvDq8ikWAM"

    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
        "accept": "audio/mpeg",
    }

    endponint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

    try:
        reponse = requests.post(endponint, json=body, headers=headers)

    except Exception as e:
        return
    
    if reponse.status_code == 200:
        return reponse.content
    else:
        return
