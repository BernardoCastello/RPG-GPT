from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

class RoleplayChat:
    def __init__(self, prompt_key: str, character_name: str, character_description: str, prompts_file: str = "prompts.json"):
        with open(prompts_file, encoding="utf-8") as f:
            prompts = json.load(f)

        if prompt_key not in prompts:
            raise ValueError(f"Prompt '{prompt_key}' não encontrado.")

        system_prompt = prompts[prompt_key]
        user_intro = f"Meu nome é {character_name}. {character_description}"

        self.history = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_intro}
        ]
        self.model = "gpt-4o"  # ou "gpt-3.5-turbo", etc.
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def send_message(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})

        trimmed_history = self.history[-6:]  # últimas 3 interações

        response = self.client.chat.completions.create(
            model=self.model,
            messages=trimmed_history
        )

        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def get_history(self):
        return self.messages
