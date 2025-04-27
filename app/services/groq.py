import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS={
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

async def get_groq_response(message:str)-> str:
    async with httpx.AsyncClient() as client:
        payload={
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role":"system",
                    "content": (
                        "You are a calm, knowledgeable, and friendly AI assistant. "
                        "Always provide clear, thoughtful, and structured answers. "
                        "If the user asks about philosophical, motivational, or spiritual topics, "
                        "give deep and wise insights inspired by Indian philosophies like Bhagavad Gita. "
                        "Keep answers concise unless asked for more detail."
                    ),
                },
                {
                    "role":"user",
                    "content": message
                },
            ],
            "temperature": 0.7,
            # "max_tokens": 1024,
            # "top_p": 1,
            # "frequency_penalty": 0,
            # "presence_penalty": 0
        }
        response = await client.post(GROQ_API_URL,headers=HEADERS,json=payload)
        response.raise_for_status()

        groq_data= response.json()
        return groq_data["choices"][0]["message"]["content"]
