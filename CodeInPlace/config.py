import os
from dotenv import load_dotenv

# Get the API key from the .env file for security
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the API key is available and raise an error if not
if not API_KEY:
    raise ValueError("API_KEY not found. Please add it to the .env file.")
else:
    print("API_KEY found.")

# Define the API URL for the Gemini model
model = 'gemini-2.0-flash'
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"

# Game Constants

GAME_LENGTH_MONTHS = 12

# Dictionary of jobs incase the AI fails
FALLBACK_CAREER_OPTIONS = {
    '1': {'name': 'Software Engineer', 'income': 7000},
    '2': {'name': 'Teacher', 'income': 4000},
    '3': {'name': 'Graphic Designer', 'income': 5000},
    '4': {'name': 'Nurse', 'income': 5500},
    '5': {'name': 'Marketing Manager', 'income': 6000},
}

