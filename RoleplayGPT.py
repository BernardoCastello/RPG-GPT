import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()

class RoleplayGPT:
    def __init__(self, prompt_path, style_key="", character_name=""):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key não encontrada. Verifique o .env.")
        openai.api_key = self.api_key

        self.character_name = character_name
        self.messages = []

        # Carrega os prompts
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompts = json.load(f)

        if style_key not in self.prompts:
            raise ValueError(f"Estilo '{style_key}' não encontrado em {prompt_path}.")

        system_prompt = self.prompts[style_key]
        self.system_message = {"role": "system", "content": system_prompt}

    def send_message(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        history = [self.system_message] + self.messages[-6:]  # Últimas 3 trocas

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=history
        )

        reply = response.choices[0].message["content"]
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def get_history(self):
        return self.messages
