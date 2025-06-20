import requests
import json
from config import API_URL, FALLBACK_JOB, FALLBACK_RENT_OPTIONS, FALLBACK_LIFE_EVENT, FALLBACK_MONTHLY_CHOICES

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

def generate_random_job(country):
    """Generates a job based on country."""
    print(f'Thinking.....\nGenerating career options for {country}.....')
    sentence_1 = f'Generate a single, common starting job for a young person in {country}.'
    sentence_2 = 'The job should be from a diverse sector and always random in nature.'
    sentence_3 = 'Provide the name and monthly income in USD, adjusted for the local cost of living. The income should be a reasonable starting salary and no less than $1000 USD per month.'
    sentence_4 = 'Example: my_career={career:Physics teacher, monthly_income:2500}'
    prompt = f'{sentence_1} {sentence_2} {sentence_3} {sentence_4}'

    schema = {
        "type": "OBJECT", "properties": {
            "name": {"type": "STRING"},
            "income": {"type": "NUMBER"}
        }, "required": ["name", "income"]
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}}

    try:
        return call_gemini(payload)
    except Exception as e:
        print(f"AI job generation failed ({e}), using fallback job.")
        return FALLBACK_JOB

def generate_rent_options(country, income):
    """Generates 5 realistic rental options based on country and income."""
    print("\nThinking of some places for you to live...")
    sentence_1 = f'A person in {country} with a monthly income of ${income} needs to find a place to live.'
    sentence_2 = 'Generate 5 realistic rental options with all bills included.'
    prompt = f"{sentence_1} {sentence_2}"

    schema = {
        "type": "OBJECT", "properties": {
            "rentals": {
                "type": "ARRAY", "items": {
                    "type": "OBJECT", "properties": {
                        "description": {"type": "STRING"},
                        "cost": {"type": "NUMBER"},
                    }, "required": ["description", "cost"]
                }
            }
        }, "required": ["rentals"]
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}}
    try:
        data = call_gemini(payload)
        return data['rentals']
    except Exception as e:
        print(f"AI rent generation failed ({e}), using fallback options.")
        return FALLBACK_RENT_OPTIONS

def generate_life_event(player_profile):
    """Generates a random, contextual life event for the player."""
    print("Thinking of a random life event...")
    sentence_1 = f'Create a realistic life event for someone who is a {player_profile['career']} in {player_profile['country']}'
    sentence_2 = 'IMPORTANT: The event must be simple, lighthearted, and appropriate for a child.  Avoid serious topics'
    sentence_3 = 'Focus on fun opportunities, minor mishaps, or social events. The financial costs should be small and manageable.'

    prompt = f"{sentence_1} {sentence_2} {sentence_3}"

    schema = {
        "type": "OBJECT", "properties": {
            "eventDescription": {"type": "STRING"},
            "cost": {"type": "NUMBER"}
        }, "required": ["eventDescription", "cost"]
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}}

    try:
        return call_gemini(payload)
    except Exception as e:
        print(f"AI life event failed ({e}), using fallback.")
        return FALLBACK_LIFE_EVENT

def generate_monthly_choices(player_profile):
    """Generates a list of optional spending choices for the month."""
    print("Thinking of some monthly spending choices...")
    sentence_1 = f'Generate 10 realistic monthly spending choices for a {player_profile['career']} in {player_profile['country']}'

    prompt = f"{sentence_1}"
    schema = {
        "type": "OBJECT", "properties": {
            "choices": {
                "type": "ARRAY", "items": {
                    "type": "OBJECT", "properties": {
                        "text": {"type": "STRING"},
                        "cost": {"type": "NUMBER"},

                    }, "required": ["text", "cost"]
                }
            }
        }, "required": ["choices"]
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}}

    try:
        data = call_gemini(payload)
        for choice in data['choices']:
            choice['cost'] = -abs(choice['cost'])
        return data['choices']
    except Exception as e:
        print(f"Monthly options failed ({e}), using fallback.")
        return FALLBACK_MONTHLY_CHOICES
