"""Rule-based coaching replies (swap for an LLM later)."""

from __future__ import annotations

import re

#chatbot using groq api and llama3.1 model

from groq import Groq
from dotenv import load_dotenv
import os

#load api key from .env file
load_dotenv()
Groq.api_key = os.getenv("GROQ_API_KEY")
client = Groq()
def coach_reply(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content