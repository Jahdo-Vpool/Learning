# Budget Craft

**Welcome to Budget Craft — where your financial adventure begins!**  
Final Project Submission – *Code in Place 2025*

In **Budget Craft**, you'll be assigned a surprise job and move out on your own for the first time. Your mission: make smart financial choices, navigate life’s twists and turns, and build enough savings to become a true **Budget Crafter**.

Choose your housing  
Manage your income  
Face unexpected, AI-generated events — from finding a stray puppy to planning a friend’s birthday party  
Can you handle whatever life throws at you and still save up 6 months’ worth of income?

Your journey starts now.

---

## Gameplay Overview

- Choose your country
- Receive a randomly generated job and income (via Google Gemini AI)
- Select a housing option based on your income
- Simulate 12 months of real-world financial decisions
- Experience unexpected life events each month
- Make a monthly spending decision that affects your savings
- Try to finish the year with at least **6 months' worth of income saved**

---

## Features

- AI-generated career, rent, spending choices, and life events based on location
- Fallback data ensures offline or error-resilient gameplay
- Friendly narrative tone designed for kids and beginners
- Typewriter-style visual effects and clean console UI

---

## Project Structure

```plaintext
budget-craft/
│
├── main.py              # Game loop and summary logic
├── config.py            # Game constants, fallbacks, API config
├── utils.py             # Typing effects, screen clearing, etc.
├── ai_services.py       # Functions to fetch AI content
├── game_logic.py        # Game setup and monthly gameplay functions
├── .env                 # Stores your Gemini API Key (do not share)
└── README.md            # This file
