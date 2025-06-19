import requests
import json
from config import API_URL, FALLBACK_CAREER_OPTIONS

def call_gemini(payload):
    """
    Function used to call the gemini service.
    It sends a payload and handles the JSON response.
    """
    headers = {'Content-Type': 'application/json'}
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    result = response.json()
    return json.loads (result['candidates'][0]['content']['parts'][0]['text'])

def generate_career_options(country):
    """Generates the career options for a given country."""
    print(f'Thinking.....\nGenerating career options for {country}.....')
