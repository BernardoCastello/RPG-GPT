import openai
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class SpeechToText:
    def __init__(self, model="whisper-1", language="pt"):
        self.model = model
        self.language = language

    def transcribe_audio(self, audio_path: str) -> str:
        """
        Envia um arquivo de áudio para a API da OpenAI e retorna a transcrição.
        """
        with open(audio_path, "rb") as audio_file:
            response = openai.Audio.transcribe(
                model=self.model,
                file=audio_file,
                language=self.language,
                response_format="text"  # pode ser json, srt, verbose_json etc.
            )
            return response.strip()
