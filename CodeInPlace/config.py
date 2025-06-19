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

# Incase the AI fails
FALLBACK_JOB= {'name': 'Teacher', 'income': 4000}

# Fallback for the new rent options (happiness removed)
FALLBACK_RENT_OPTIONS = [
    {"description": "A small room in a shared house far from the city center.", "cost": 800},
    {"description": "A decent studio apartment with a reasonable commute.", "cost": 1200},
    {"description": "A modern one-bedroom apartment downtown.", "cost": 2000},
    {"description": "Living with parents to save money.", "cost": 200},
    {"description": "A stylish loft with great amenities.", "cost": 2500}
]

# Fallback for the monthly spending choices
FALLBACK_MONTHLY_CHOICES = [
    {"text": "Buy new running shoes", "cost": -120},
    {"text": "Subscribe to Apple Music", "cost": -10},
    {"text": "Cancel your streaming service", "cost": 0},
    {"text": "Buy daily coffee all month", "cost": -75},
    {"text": "Join a gym", "cost": -60},
    {"text": "Eat out every weekend", "cost": -200},
    {"text": "Donate to a charity", "cost": -50},
    {"text": "Buy a video game", "cost": -60},
    {"text": "Take a short trip", "cost": -300},
    {"text": "Buy books for self-study", "cost": -40},
]

# Fallback for the random life event
FALLBACK_LIFE_EVENT = {
    "eventDescription": "You received a surprise refund from your internet provider!",
    "cost": 50
}