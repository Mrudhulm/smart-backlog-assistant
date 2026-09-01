from google import genai
from config.settings import GEMINI_API_KEY, DEFAULT_MODEL
from src.validator import BacklogOutput

class AIBacklogClient:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = DEFAULT_MODEL

    def generate_backlog(self, raw_text: str) -> BacklogOutput:
        prompt = f"""
You are an expert Agile Product Manager and Technical Architect. 
Your job is to analyze unstructured engineering meeting notes or PRDs and break them down into structured, high-quality, and actionable user stories.

RAW INPUT TEXT:
----------------
{raw_text}
----------------
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": BacklogOutput,
                    "temperature": 0.2,
                },
            )
            return response.parsed
        except Exception as e:
            raise RuntimeError(f"Failed to communicate with Gemini API or parse response: {e}")
