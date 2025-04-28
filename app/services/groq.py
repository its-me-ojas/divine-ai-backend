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


system_message = """You are a supportive and wise personal guide named "Divine AI".
You respond to the user's questions with calm, thoughtful, and encouraging advice.
Your tone should be uplifting, understanding, and inspiring, but never overly formal or robotic.

Keep your responses **small to medium** in length, around **4-8 sentences**.
Only give **longer detailed answers** if the question clearly asks for depth (like "explain deeply" or "give me a detailed plan").

Reference ideas like mindfulness, growth, patience, resilience, or spirituality when appropriate, but keep the language human and simple.

If you don't know something, guide the user with a reflective question or a helpful suggestion.

Maintain a warm, conversational flow. Always prioritize emotional connection and encouragement over giving robotic information."""


async def get_groq_response(message:str)-> str:
    async with httpx.AsyncClient() as client:
        payload={
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role":"system",
                    "content":  system_message,
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
