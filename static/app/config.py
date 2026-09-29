import os
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


WORKOUT_MODEL = os.getenv(
    "WORKOUT_MODEL",
    "gemini-3.1-pro-preview"
)


TIP_MODEL = os.getenv(
    "TIP_MODEL",
    "gemini-2.5-flash"
)


ADMIN_KEY = os.getenv(
    "ADMIN_KEY",
    "fitbuddy-admin"
)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./fitbuddy.db"
)