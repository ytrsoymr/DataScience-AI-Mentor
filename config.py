import os
from dotenv import load_dotenv
import uuid

# Load environment variables from a .env file
load_dotenv()

# Google GenAI API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# SQLite Database File Path
DB_PATH = os.getenv("DB_PATH", "chats_data/sqlite.db")  # Default file if not set

# LangChain Configuration
MODEL_NAME = "gemini-1.5-pro"
TEMP = 0.7  # Model temperature

# Function to generate a new session ID (UUID)
def generate_session_id():
    return str(uuid.uuid4())
