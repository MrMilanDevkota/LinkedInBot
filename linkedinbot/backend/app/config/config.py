import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
            self.GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
    
    RESUME_DATA_FILE = 'resume_data.json'


config = Config()

