import requests
import json
from config import API_URL, FALLBACK_CAREER_OPTIONS, FALLBACK_RENT_OPTIONS, FALLBACK_LIFE_EVENT, FALLBACK_MONTHLY_CHOICES

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
    sentence_1 = 'Generate a list of 5 common careers for {country}.'
    sentence_2 = 'For each career, provide: name and average monthly income in USD.'
    sentence_3 = 'Example: my_career={career:Physics teacher, monthly_income:3200}'
    prompt = f'{sentence_1} {sentence_2} {sentence_3}'

    schema = {
        "type": "OBJECT", "properties": {
            "careers": {
                "type": "ARRAY", "items": {
                    "type": "OBJECT", "properties": {
                        "name": {"type": "STRING"},
                        "income": {"type": "NUMBER"}
                    }, "required": ["name", "income"]
                }
            }
        }, "required": ["careers"]
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}}

    try:
        data = call_gemini(payload)
        return {str(i+1): career for i, career in enumerate(data['career'])}
    except Exception as e:
        print(f"AI career generation failed ({e}), using fallback career options.")
        return FALLBACK_CAREER_OPTIONS

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
                        "happinessEffect": {"type": "NUMBER"}
                    }, "required": ["description", "cost", "happinessEffect"]
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
    sentence_2 = 'Provide 3 choices for the player to make.'
    sentence_3 = 'IMPORTANT: The event must be simple, lighthearted, and appropriate for a child.  Avoid serious topics'
    sentence_4 = 'Focus on fun opportunities, minor mishaps, or social events. The financial costs should be small and manageable.'

    prompt = f"{sentence_1} {sentence_2} {sentence_3} {sentence_4}"

    schema = {
        "type": "OBJECT", "properties": {
            "eventDescription": {"type": "STRING"},
            "choices": {
                "type": "ARRAY", "items": {
                    "type": "OBJECT", "properties": {
                        "text": {"type": "STRING"},
                        "cost": {"type": "NUMBER"},
                        "happinessChange": {"type": "NUMBER"}
                    }, "required": ["text", "cost", "happinessChange"]
                }
            }
        }, "required": ["eventDescription", "choices"]
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
                        "happinessChange": {"type": "NUMBER"}
                    }, "required": ["text", "cost", "happinessChange"]
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
