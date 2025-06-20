# This file is responsible for all communication with the Gemini API.
# It contains functions that generate dynamic, AI-powered content for the game.

import requests
import json
# Import the API URL and all fallback data from the config file.
# This keeps configuration separate from the service logic.
from config import API_URL, FALLBACK_JOB, FALLBACK_RENT_OPTIONS, FALLBACK_LIFE_EVENT, FALLBACK_MONTHLY_CHOICES


def call_gemini(payload):
    """
    A generic function used to call the Gemini API service.
    It sends a pre-formatted payload and handles the JSON response.
    This function is the central point of communication with the AI.
    """
    # Set the header to tell the server we are sending data in JSON format.
    # This is a requirement for the Gemini API.
    headers = {'Content-Type': 'application/json'}

    # Send the request to the API URL using a POST request, which is used for sending data.
    # The payload (a Python dictionary) is converted to a JSON string.
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    # This is a critical error-checking step. If the server returns an error
    # (like 404 Not Found or 500 Server Error), it will raise an exception.
    response.raise_for_status()

    # If the request was successful, parse the JSON response from the server into a Python dictionary.
    result = response.json()

    # The Gemini API returns the desired JSON as a string within a nested structure.
    # This line navigates through the response dictionary to extract that string
    # and then parses it into the final, clean Python dictionary that the game can use.
    return json.loads(result['candidates'][0]['content']['parts'][0]['text'])


def generate_random_job(country):
    """Generates a single random job and income based on the player's country."""
    print(f'Thinking.....\nGenerating career options for {country}.....')

    # Construct a detailed, multi-part prompt to guide the AI.
    # Providing specific instructions and an example helps improve the quality of the response.
    sentence_1 = f'Generate a single, common starting job for a young person in {country}.'
    sentence_2 = 'The job should be from a diverse sector and always random in nature.'
    sentence_3 = 'Provide the name and monthly income in USD, adjusted for the local cost of living. The income should be a reasonable starting salary and no less than $1000 USD per month.'
    sentence_4 = 'Example: my_career={{career:Physics teacher, monthly_income:2500}}'
    prompt = f'{sentence_1} {sentence_2} {sentence_3} {sentence_4}'

    # Define the exact JSON structure (a schema) that the AI's response must follow.
    # This enforces consistency and makes the response easy and reliable to parse.
    schema = {
        "type": "OBJECT", "properties": {
            "name": {"type": "STRING"},
            "income": {"type": "NUMBER"}
        }, "required": ["name", "income"]
    }
    # Create the final payload, combining the prompt and the required response schema.
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}}

    try:
        # Attempt to call the API with the constructed payload.
        return call_gemini(payload)
    except Exception as e:
        # If the API call fails for any reason (e.g., network error, bad API key),
        # this block will execute, preventing the game from crashing.
        print(f"AI job generation failed ({e}), using fallback job.")
        # Return a safe, predefined value from the config file.
        return FALLBACK_JOB


def generate_rent_options(country, income):
    """Generates 5 realistic rental options based on country and income."""
    print("\nThinking of some places for you to live...")
    sentence_1 = f'A person in {country} with a monthly income of ${income} needs to find a place to live.'
    sentence_2 = 'Generate 5 realistic rental options with all bills included.'
    prompt = f"{sentence_1} {sentence_2}"

    # Define the required JSON structure for a list of rental options.
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
        # Call the API and extract the 'rentals' list from the returned data.
        data = call_gemini(payload)
        return data['rentals']
    except Exception as e:
        # If the API call fails, return the predefined list of fallback options.
        print(f"AI rent generation failed ({e}), using fallback options.")
        return FALLBACK_RENT_OPTIONS


def generate_life_event(player_profile):
    """Generates a random, contextual, and choiceless life event for the player."""
    print("Thinking of a random life event...")
    # Construct a prompt with very specific instructions for the AI to ensure
    # the event is kid-friendly and follows the game's mechanics.
    sentence_1 = f"Create a realistic life event for someone who is a {player_profile['career']} in {player_profile['country']}"
    sentence_2 = 'IMPORTANT: The event must be simple, lighthearted, and appropriate for a child. Avoid serious topics.'
    sentence_3 = 'Focus on fun opportunities, minor mishaps, or social events. The financial costs should be small and manageable.'
    prompt = f"{sentence_1} {sentence_2} {sentence_3}"

    # Define a simple structure for the event: a description and a direct cost.
    # The cost can be positive (a gain) or negative (a loss).
    schema = {
        "type": "OBJECT", "properties": {
            "eventDescription": {"type": "STRING"},
            "cost": {"type": "NUMBER"}
        }, "required": ["eventDescription", "cost"]
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}}

    try:
        # Call the API to get the event.
        return call_gemini(payload)
    except Exception as e:
        # Return a safe, predefined event if the API call fails.
        print(f"AI life event failed ({e}), using fallback.")
        return FALLBACK_LIFE_EVENT


def generate_monthly_choices(player_profile):
    """Generates a list of optional spending choices for the month."""
    print("Thinking of some monthly spending choices...")
    sentence_1 = f"Generate 10 realistic monthly spending choices for a {player_profile['career']} in {player_profile['country']}"
    prompt = f"{sentence_1}"

    # Define the structure for the list of choices.
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
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema}}

    try:
        # Get the data from the API.
        data = call_gemini(payload)
        # Loop through the choices and ensure the cost is a negative number, as it's an expense.
        # This prevents the AI from creating a choice that accidentally gives the player money.
        for choice in data['choices']:
            choice['cost'] = -abs(choice['cost'])
        return data['choices']
    except Exception as e:
        # If the API fails, return the hard-coded list of choices.
        print(f"Monthly options failed ({e}), using fallback.")
        return FALLBACK_MONTHLY_CHOICES
