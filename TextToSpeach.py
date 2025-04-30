import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
from io import BytesIO

# Carrega variáveis do .env
load_dotenv()

class AzureTextToSpeechProcessor:
    def __init__(self, text: str, voice: str):
        self.text = text
        self.voice = voice
        self.subscription_key = os.getenv("Azure_Key")
        self.region = os.getenv("Azure_Region")

        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.subscription_key,
            region=self.region
        )
        self.speech_config.speech_synthesis_voice_name = self.voice

    def synthesize_speech(self) -> bytes:
        """
        Converte o texto em fala e retorna os bytes do áudio gerado.
        """
        # Stream de saída para capturar o áudio
        stream = speechsdk.audio.PullAudioOutputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=stream)

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )

        result = synthesizer.speak_text_async(self.text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_data = BytesIO()
            chunk = bytearray(4096)
            bytes_read = stream.read(chunk)

            while bytes_read > 0:
                audio_data.write(chunk[:bytes_read])
                bytes_read = stream.read(chunk)

            return audio_data.getvalue()

        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            error_message = f"Erro: {cancellation_details.reason}"
            if cancellation_details.error_details:
                error_message += f" | Detalhes: {cancellation_details.error_details}"
            raise Exception(error_message)
