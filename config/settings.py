import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # Change this line inside config/settings.py:
    # Alternative fallback option:
    # Change this line inside config/settings.py:
    MODEL_NAME = "gemini-1.5-flash"  # Fastest, optimized model for real-time recommendations
    
    @classmethod
    def validate_config(cls):
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == "YOUR_ACTUAL_API_KEY_HERE":
            return False
        return True