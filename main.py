import os
import warnings
import requests

# Suppress Pydantic V1 compatibility warning BEFORE importing elevenlabs
warnings.filterwarnings("ignore", message=".*Pydantic V1 functionality.*")

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

def STS(url):
    key = os.getenv("ELEVENLABS_API_KEY") 
    client = ElevenLabs(api_key=key)
    result = client.speech_to_text.convert(
        model_id="scribe_v2",
        language_code="en",
        cloud_storage_url=url
    )
    return result.text

files = get_audio_files()
'''for file in files:
    print("Processing file:", file)
    print(STS(file))'''