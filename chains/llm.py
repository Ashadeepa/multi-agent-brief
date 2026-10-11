"""Shared Gemini model factory."""
import os

from langchain_google_genai import ChatGoogleGenerativeAI

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


def get_llm() -> ChatGoogleGenerativeAI:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    return ChatGoogleGenerativeAI(model=MODEL, google_api_key=key)
