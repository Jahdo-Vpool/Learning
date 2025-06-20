import random
import time
from config import GAME_LENGTH_MONTHS
from utils import clear_screen, print_separator, typewriter_effect
from ai_services import generate_random_job, generate_life_event, generate_monthly_choices, generate_rent_options

def setup_game():
    """Initializes the game by getting player info, career, and housing."""
    clear_screen()
    typewriter_effect("Welcome to AI Finance Quest!")
    print_separator()
    name = input("What is your name? ")
    country = input("Which country are you from? ")

    # Job Assignment
    assigned_job = generate_random_job(country)

    clear_screen()
    print_separator()
    typewriter_effect("The results are in!")
    typewriter_effect(f"Your first job is: {assigned_job['name']}")
    typewriter_effect(f"Your starting monthly income will be: ${assigned_job['income']:,}")
    print_separator()
    input("Press Enter to continue...")

    # Rent Choice
    clear_screen()
    typewriter_effect("To start your new job, you need to move out.")
    typewriter_effect("It's time for your first big financial decision: choosing where to live.")

    rent_options = generate_rent_options(country, assigned_job['income'])

    print_separator()
    print("Choose your housing (all options include bills):\n")
    for i, option in enumerate(rent_options):
        print(f"  [{i + 1}] {option['description']} (Cost: ${option['cost']:,}/mo)")

    rent_choice_key = 0
    while rent_choice_key not in range(1, len(rent_options) + 1):
        try:
            # Prompt for input on its own line
            rent_choice_str = input("Enter your choice: ")
            rent_choice_key = int(rent_choice_str)
            # Add a check to print the error message only if the number is out of range
            if rent_choice_key not in range(1, len(rent_options) + 1):
                print("Invalid input. Please choose a number from the list.")
        except ValueError:
            # Error message for non-numeric input
            print("Invalid input. Please enter a number.")

    selected_rent = rent_options[rent_choice_key - 1]

    print_separator()
    typewriter_effect(f"You've chosen: \"{selected_rent['description']}\"")
    typewriter_effect(f"This will cost ${selected_rent['cost']:,} each month. A wise choice!")
    print_separator()
    input("Press Enter to begin your first month...")

    # Initialize player profile with an assigned job and chosen rent
    return {
        'name': name, 'country': country, 'career': assigned_job['name'],
        'income': assigned_job['income'],
        'rent_expense': selected_rent['cost'],  # Main fixed expense
        'savings': 0,
        'month': 1,
        'history': []
    }

def display_stats(player):
    """Displays the player's current financial stats."""
    print_separator()
    print(f"--- Month {player['month']} of {GAME_LENGTH_MONTHS} ---")
    print(f"Player: {player['name']} | Career: {player['career']}")
    print("-" * 20)
    print(f"Savings: ${player['savings']:,}")
    print_separator()

def monthly_cycle(player):
    """Runs one full month of the game, including income, rent, events, and choices."""
    clear_screen()
    display_stats(player)
    input("Press Enter to start the month...")
    clear_screen()

    player['savings'] += player['income']
    typewriter_effect(f"Payday! +${player['income']:,} has been added to your account.")
    time.sleep(1)

    player['savings'] -= player['rent_expense']
    typewriter_effect(f"Rent is due. -${player['rent_expense']:,} has been paid.")
    time.sleep(2)

    # 50% chance of a random life event occurring
    if random.random() < 0.5:
        event = generate_life_event(player)
        print_separator()
        typewriter_effect(f"LIFE EVENT: {event['eventDescription']}")

        # Apply the financial consequence automatically
        player['savings'] += event['cost']

        if event['cost'] >= 0:
            typewriter_effect(f"You gained ${event['cost']:,}!")
        else:
            typewriter_effect(f"You lost ${abs(event['cost']):,}!")

        time.sleep(2)

    # Optional monthly spending choice
    print_separator()
    typewriter_effect("Now choose one extra activity this month.")
    options = generate_monthly_choices(player)
    for i, opt in enumerate(options):
        # FIXED: Added the closing parenthesis
        print(f"  [{i + 1}] {opt['text']} (Cost: ${abs(opt['cost']):,})")

    pick = 0
    # FIXED: Made the loop range dynamic based on the number of options
    while pick not in range(1, len(options) + 1):
        try:
            pick_str = input(f"Your choice (1-{len(options)}): ")
            pick = int(pick_str)
            if pick not in range(1, len(options) + 1):
                print(f"Invalid input. Please choose a number from 1 to {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    act = options[pick - 1]
    player['savings'] += act['cost']
    time.sleep(1)

    player['history'].append({
        'month': player['month'], 'savings': player['savings']
    })
    return player


def check_game_over(player):
    """Checks for conditions that would end the game."""
    if player['savings'] < -2000:
        print("\nYour debt has become unmanageable. Game over.")
        return True
    return False



