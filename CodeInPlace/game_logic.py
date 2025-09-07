
import random, time
from typing import List, Dict, Any
from state import GameState
from config import GAME_LENGTH_MONTHS
from utils import clear_screen, print_separator, typewriter_effect
from ai_services import (
    generate_random_job,
    generate_life_event,
    generate_monthly_choices,
    generate_rent_options,
)

# --- Game Logic Functions ---

def setup_game() -> GameState:
    """Initializes the game by getting player info, assigning a job, and setting housing."""
    clear_screen()
    typewriter_effect("Welcome to Budget Craft!")
    print_separator()
    name = input("What is your name? ")
    country = input("Where do you reside in this beautiful world? ")

    # --- Job Assignment ---
    assigned_job = generate_random_job(country)  # {"name": str, "income": number}

    # Reveal job
    clear_screen()
    print_separator()
    typewriter_effect("The results are in!")
    typewriter_effect(f"Your first job is: {assigned_job['name']}")
    typewriter_effect(f"Your starting monthly income will be: ${int(assigned_job['income']):,}")
    print_separator()
    input("Press Enter to continue...")

    # --- Rent Choice ---
    clear_screen()
    typewriter_effect("To start your new job, you need to move out.")
    typewriter_effect("It's time for your first big financial decision: choosing where to live.")

    rent_options = generate_rent_options(country, int(assigned_job['income']))  # list[{description, cost}]

    print_separator()
    print("Choose your housing (all options include bills):\n")
    for i, option in enumerate(rent_options, start=1):
        print(f"  [{i}] {option['description']} (Cost: ${int(option['cost']):,}/mo)")

    rent_choice_key = 0
    while rent_choice_key not in range(1, len(rent_options) + 1):
        try:
            rent_choice_key = int(input("Enter your choice: "))
            if rent_choice_key not in range(1, len(rent_options) + 1):
                print("Invalid input. Please choose a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    selected_rent = rent_options[rent_choice_key - 1]

    print_separator()
    typewriter_effect(f"You've chosen: \"{selected_rent['description']}\"")
    typewriter_effect(f"This will cost ${int(selected_rent['cost']):,} each month. A wise choice!")
    print_separator()
    input("Press Enter to begin your first month...")

    # Return a GameState (note field names!)
    return GameState(
        name=name,
        country=country,
        job_title=assigned_job['name'],
        monthly_income=int(assigned_job['income']),
        rent_expense=int(selected_rent['cost']),
        savings=0,
        month=1,
        history=[],
    )

def display_stats(state: GameState):
    """Displays the player's current financial stats."""
    print_separator()
    print(f"--- Month {state.month} of {GAME_LENGTH_MONTHS} ---")
    print(f"Player: {state.name} | Career: {state.job_title}")
    print("-" * 20)
    print(f"Savings: ${state.savings:,}")
    print_separator()

def monthly_cycle(state: GameState) -> GameState:
    """Runs one full month of the game, including income, rent, events, and choices (CLI)."""
    clear_screen()
    display_stats(state)
    input("Press Enter to start the month...")
    clear_screen()

    # --- Income and Fixed Expenses ---
    state.savings += int(state.monthly_income)
    typewriter_effect(f"Payday! +${int(state.monthly_income):,} has been added to your account.")
    time.sleep(1)

    state.savings -= int(state.rent_expense)
    typewriter_effect(f"Rent is due. -${int(state.rent_expense):,} has been paid.")
    time.sleep(2)

    # --- Random Life Event (50%) ---
    if random.random() < 0.5:
        # Your AI expects a profile dict; pass what it needs
        event = generate_life_event({"career": state.job_title, "country": state.country})
        print_separator()
        typewriter_effect(f"LIFE EVENT: {event['eventDescription']}")
        delta = int(event['cost'])
        state.savings += delta
        if delta >= 0:
            typewriter_effect(f"You gained ${delta:,}!")
        else:
            typewriter_effect(f"You lost ${abs(delta):,}!")
        time.sleep(2)

    # --- Optional Monthly Spending ---
    print_separator()
    typewriter_effect("Now choose one extra activity this month.")
    options: List[Dict[str, Any]] = generate_monthly_choices({"career": state.job_title, "country": state.country})
    # enforce negative costs (expenses)
    for opt in options:
        opt['cost'] = -abs(int(opt['cost']))

    for i, opt in enumerate(options, start=1):
        print(f"  [{i}] {opt['text']} (Cost: ${abs(int(opt['cost'])):,})")

    pick = 0
    while pick not in range(1, len(options) + 1):
        try:
            pick = int(input(f"Your choice (1-{len(options)}): "))
            if pick not in range(1, len(options) + 1):
                print(f"Invalid input. Please choose a number from 1 to {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    act = options[pick - 1]
    state.savings += int(act['cost'])
    time.sleep(1)

    # Record month-end snapshot
    state.history.append({
        'month': state.month,
        'savings': state.savings,
    })
    return state

def check_game_over(state: GameState) -> bool:
    """Checks for conditions that would end the game."""
    if state.savings < -2000:
        print("\nYour debt has become unmanageable. Game over.")
        return True
    return False




