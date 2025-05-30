# llm and gemini logic here 
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv

# Import the Config class from  config.py file
from app.config.config import Config

class LLMController:
    def __init__(self):
        self.config = Config()
        os.environ["GOOGLE_API_KEY"] = self.config.GEMINI_API_KEY


    def setup_llm(self):
        llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.environ["GOOGLE_API_KEY"], 
            temperature=0.7
        )
        return llm