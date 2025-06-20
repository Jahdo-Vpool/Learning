# Import necessary modules and functions from other files.
# 'random' is for the chance-based life events.
# 'time' is for pausing the game to improve readability.
# Functions and constants are imported from our other custom modules.
import random
import time
from config import GAME_LENGTH_MONTHS
from utils import clear_screen, print_separator, typewriter_effect
from ai_services import generate_random_job, generate_life_event, generate_monthly_choices, generate_rent_options

# --- Game Logic Functions ---

def setup_game():
    """Initializes the game by getting player info, assigning a job, and setting housing."""
    # Start with a clean screen and a welcome message.
    clear_screen()
    typewriter_effect("Welcome to AI Finance Quest!")
    print_separator()
    name = input("What is your name? ")
    country = input("Which country are you from? ")

    # --- Job Assignment ---
    # Call the AI service to get a random job based on the player's country.
    assigned_job = generate_random_job(country)

    # Display the assigned job and income to the player.
    clear_screen()
    print_separator()
    typewriter_effect("The results are in!")
    typewriter_effect(f"Your first job is: {assigned_job['name']}")
    typewriter_effect(f"Your starting monthly income will be: ${assigned_job['income']:,}")
    print_separator()
    # Pause the game and wait for the player to press Enter before continuing.
    input("Press Enter to continue...")

    # --- Rent Choice ---
    # Guide the player through their first major financial decision.
    clear_screen()
    typewriter_effect("To start your new job, you need to move out.")
    typewriter_effect("It's time for your first big financial decision: choosing where to live.")

    # Call the AI service to get rent options based on the player's income and country.
    rent_options = generate_rent_options(country, assigned_job['income'])

    print_separator()
    print("Choose your housing (all options include bills):\n")
    # Loop through and display each rent option with a number.
    for i, option in enumerate(rent_options):
        print(f"  [{i + 1}] {option['description']} (Cost: ${option['cost']:,}/mo)")

    # This loop ensures the player enters a valid number corresponding to a rent option.
    rent_choice_key = 0
    while rent_choice_key not in range(1, len(rent_options) + 1):
        try:
            # Get the user's choice as a string.
            rent_choice_str = input("Enter your choice: ")
            # Convert the string to an integer. This will raise a ValueError if it's not a number.
            rent_choice_key = int(rent_choice_str)
            # Check if the number is within the valid range of choices.
            if rent_choice_key not in range(1, len(rent_options) + 1):
                print("Invalid input. Please choose a number from the list.")
        except ValueError:
            # This block runs if the user enters text that cannot be converted to an integer.
            print("Invalid input. Please enter a number.")

    # Get the chosen rent dictionary from the list using the player's choice (minus 1 for list indexing).
    selected_rent = rent_options[rent_choice_key - 1]

    # --- Confirmation and Player Profile Creation ---
    print_separator()
    typewriter_effect(f"You've chosen: \"{selected_rent['description']}\"")
    typewriter_effect(f"This will cost ${selected_rent['cost']:,} each month. A wise choice!")
    print_separator()
    input("Press Enter to begin your first month...")

    # Create and return the main 'player' dictionary, which will hold the game state.
    return {
        'name': name,
        'country': country,
        'career': assigned_job['name'],
        'income': assigned_job['income'],
        'rent_expense': selected_rent['cost'],  # This is now the main fixed expense.
        'savings': 0,
        'month': 1,
        'history': []  # This list can be used later to track progress over time.
    }

def display_stats(player):
    """Displays the player's current financial stats."""
    # This function provides a consistent status update at the start of each month.
    print_separator()
    print(f"--- Month {player['month']} of {GAME_LENGTH_MONTHS} ---")
    print(f"Player: {player['name']} | Career: {player['career']}")
    print("-" * 20)
    # The ':, ' formats the number with commas for thousands, improving readability.
    print(f"Savings: ${player['savings']:,}")
    print_separator()

def monthly_cycle(player):
    """Runs one full month of the game, including income, rent, events, and choices."""
    clear_screen()
    display_stats(player)
    input("Press Enter to start the month...")
    clear_screen()

    # --- Income and Fixed Expenses ---
    # Add income to savings.
    player['savings'] += player['income']
    typewriter_effect(f"Payday! +${player['income']:,} has been added to your account.")
    time.sleep(1)

    # Subtract the monthly rent expense.
    player['savings'] -= player['rent_expense']
    typewriter_effect(f"Rent is due. -${player['rent_expense']:,} has been paid.")
    time.sleep(2)

    # --- Random Life Event ---
    # 'random.random()' generates a float between 0.0 and 1.0.
    # This 'if' statement gives a 50% chance for a life event to occur each month.
    if random.random() < 0.5:
        event = generate_life_event(player)
        print_separator()
        typewriter_effect(f"LIFE EVENT: {event['eventDescription']}")

        # Apply the financial consequence of the event automatically.
        player['savings'] += event['cost']

        # Display a different message depending on whether it was a gain or a loss.
        if event['cost'] >= 0:
            typewriter_effect(f"You gained ${event['cost']:,}!")
        else:
            # 'abs()' shows the cost as a positive number, which is more natural to read.
            typewriter_effect(f"You lost ${abs(event['cost']):,}!")
        time.sleep(2)

    # --- Optional Monthly Spending ---
    # This section allows the player to make an optional spending choice.
    print_separator()
    typewriter_effect("Now choose one extra activity this month.")
    options = generate_monthly_choices(player)
    for i, opt in enumerate(options):
        print(f"  [{i + 1}] {opt['text']} (Cost: ${abs(opt['cost']):,})")

    # This loop validates the player's input for the spending choice.
    pick = 0
    while pick not in range(1, len(options) + 1):
        try:
            pick_str = input(f"Your choice (1-{len(options)}): ")
            pick = int(pick_str)
            if pick not in range(1, len(options) + 1):
                print(f"Invalid input. Please choose a number from 1 to {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Get the chosen activity from the list and apply its cost to savings.
    act = options[pick - 1]
    player['savings'] += act['cost']
    time.sleep(1)

    # Record the state at the end of the month for potential future features (like graphing progress).
    player['history'].append({
        'month': player['month'],
        'savings': player['savings']
    })
    # Return the updated player dictionary to the main game loop.
    return player

def check_game_over(player):
    """Checks for conditions that would end the game."""
    # If the player's savings drop below a certain threshold, the game ends.
    if player['savings'] < -2000:
        print("\nYour debt has become unmanageable. Game over.")
        return True
    # If no game-over condition is met, return False to continue the game.
    return False



