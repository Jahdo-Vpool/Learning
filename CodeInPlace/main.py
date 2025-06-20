# Import the necessary functions and constants from the other modules.
# This keeps the main file clean and focused on the high-level game loop.
from config import GAME_LENGTH_MONTHS
from utils import clear_screen, print_separator, typewriter_effect
from game_logic import setup_game, monthly_cycle, check_game_over

# --- Main Application ---

def main():
    """The main entry point for the AI Finance Quest game."""
    # Call setup_game() once at the beginning to initialize the player's profile.
    # The returned 'player' dictionary will hold all the game state.
    player = setup_game()

    # This loop runs the game for the number of months defined in the config file.
    # The 'for...else' structure is used to handle the end-of-game summary cleanly.
    for month_num in range(1, GAME_LENGTH_MONTHS + 1):
        # Set the current month in the player's profile.
        player['month'] = month_num

        # Call the main gameplay function for the current month.
        # This returns the updated player profile.
        player = monthly_cycle(player)

        # After each month, check if a game-over condition has been met.
        if check_game_over(player):
            # If the game is over, exit the loop immediately.
            # This prevents the final summary from being displayed for a lost game.
            break

        # If it's not the last month, pause and wait for the user to proceed.
        if player['month'] < GAME_LENGTH_MONTHS:
            print_separator()
            input("Press Enter to continue to the next month...")

    # --- Game Summary ---
    # The 'else' block of a 'for' loop is a special feature in Python.
    # It runs ONLY if the loop completes naturally (i.e., it was not exited by a 'break').
    # This is perfect for showing the summary only if the player successfully finishes the year.
    else:
        clear_screen()
        print_separator()
        print("Year complete! Final Summary:")
        print(f"Final Savings: ${player['savings']:,}")
        print_separator()

        # Calculate the win condition based on the player's income.
        win_condition = player['income'] * 6

        # Check the final savings against the win condition and display the appropriate outcome.
        if player['savings'] >= win_condition:
            typewriter_effect(
                f"WINNER! You saved ${player['savings']:,}, reaching the goal of ${win_condition:,} (6 months' pay).")
            typewriter_effect("You are a financial superstar!")
        elif player['savings'] > 0:
            typewriter_effect(f"Great effort! You ended the year with positive savings of ${player['savings']:,}.")
            typewriter_effect("You've built a solid financial foundation.")
        else:
            typewriter_effect("It was a tough year. You ended the year in debt.")
            typewriter_effect("Use this as a learning experience and try again!")


# This is a standard Python construct.
# It ensures that the main() function is called only when this script is run directly,
# not when it's imported as a module into another file.
if __name__ == "__main__":
    main()
