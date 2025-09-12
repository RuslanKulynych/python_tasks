import datetime
import os
from pathlib import Path


# ----------------------------
# DATA STORAGE CONFIG
# ----------------------------

OUTPUT_FILE = Path("news_feed.txt")


# ----------------------------
# HELPERS
# ----------------------------

def append_to_file(record: str):
    """Append a formatted record to the output file."""
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(record + "\n" + "-" * 40 + "\n")
    print("\n✅ Record added to news feed!\n")


# ----------------------------
# NEWS RECORD
# ----------------------------

def publish_news():
    """Collect news data from user and publish it."""
    text = input("Enter news text: ")
    city = input("Enter city: ")
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    record = f"NEWS -------------------------\n{text}\nCity: {city}, {date}"
    append_to_file(record)


# ----------------------------
# PRIVATE AD RECORD
# ----------------------------

def publish_private_ad():
    """Collect ad data, calculate days left, and publish it."""
    text = input("Enter ad text: ")
    exp_date_str = input("Enter expiration date (YYYY-MM-DD): ")

    try:
        exp_date = datetime.datetime.strptime(exp_date_str, "%Y-%m-%d").date()
        days_left = (exp_date - datetime.date.today()).days
        if days_left < 0:
            days_left_text = "Expired!"
        else:
            days_left_text = f"{days_left} days left"
    except ValueError:
        days_left_text = "Invalid date format"
    
    record = f"PRIVATE AD -------------------\n{text}\nExpires: {exp_date_str} ({days_left_text})"
    append_to_file(record)


# ----------------------------
# UNIQUE CUSTOM TYPE (Example: Motivational Quote)
# ----------------------------

def publish_quote():
    """Collect a quote and author, publish with weekday info."""
    quote = input("Enter your motivational quote: ")
    author = input("Enter author: ")
    weekday = datetime.datetime.now().strftime("%A")
    record = f"QUOTE OF THE DAY ------------\n\"{quote}\"\n— {author}, shared on {weekday}"
    append_to_file(record)


# ----------------------------
# MAIN MENU
# ----------------------------

def show_menu():
    """Display menu and handle user choice."""
    while True:
        print("\n=== USER NEWS FEED ===")
        print("1. Publish News")
        print("2. Publish Private Ad")
        print("3. Publish Motivational Quote")
        print("4. Exit")
        choice = input("Choose option (1-4): ")

        if choice == "1":
            publish_news()
        elif choice == "2":
            publish_private_ad()
        elif choice == "3":
            publish_quote()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("❌ Invalid option. Please try again.")


# ----------------------------
# ENTRY POINT
# ----------------------------

if __name__ == "__main__":
    show_menu()
