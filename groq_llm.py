import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_llm(temperature=0.6):
    if os.getenv("GROQ_API_KEY") is None:
        raise RuntimeError("GROQ_API_KEY not found")

    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=temperature
    )
    