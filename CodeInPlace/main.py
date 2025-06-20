from config import GAME_LENGTH_MONTHS
from utils import clear_screen, print_separator, typewriter_effect
from game_logic import setup_game, monthly_cycle, check_game_over


# Main Application

def main():
    """The main entry point for the AI Finance Quest game."""
    player = setup_game()

    # --- FIXED: Using a more robust 'for...else' loop structure ---
    # This ensures the game cycles through each month correctly and then
    # proceeds to the summary only after the loop is fully completed.
    for month_num in range(1, GAME_LENGTH_MONTHS + 1):
        player['month'] = month_num  # Set the current month for the cycle

        player = monthly_cycle(player)

        if check_game_over(player):
            # If the game is over, break the loop immediately
            break

            # At the end of a successful month, ask to continue
        if player['month'] < GAME_LENGTH_MONTHS:
            print_separator()
            input("Press Enter to continue to the next month...")

    # --- Game Summary ---
    # The 'else' block for a 'for' loop runs ONLY if the loop completes
    # without being exited by a 'break' statement.
    else:
        clear_screen()
        print_separator()
        print("Year complete! Final Summary:")
        print(f"Final Savings: ${player['savings']:,}")
        print_separator()

        # Win condition based on saving 6 months' worth of income
        win_condition = player['income'] * 6

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


if __name__ == "__main__":
    main()
