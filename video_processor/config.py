import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/railway")

    # APIs
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    FISH_AUDIO_API_KEY = os.getenv("FISH_AUDIO_API_KEY")
    HEDRA_API_KEY = os.getenv("HEDRA_API_KEY")
    RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
    LUMA_API_KEY = os.getenv("LUMA_API_KEY")
    YOUTUBE_CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")

    # Suno (Wrapper & Fallback)
    SUNO_API_URL = os.getenv("SUNO_API_URL", "http://localhost:8000") # Setup your suno-api-fixed URL here
    MANUAL_SUNO_MODE = os.getenv("MANUAL_SUNO_MODE", "false").lower() == "true"

    # Paths
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
    TEMP_DIR = os.path.join(OUTPUT_DIR, "temp")

    @classmethod
    def validate(cls):
        # Add crucial validation logic here if needed
        pass

os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
os.makedirs(Config.TEMP_DIR, exist_ok=True)
