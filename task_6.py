import datetime
from pathlib import Path
import os


OUTPUT_FILE = Path("news_feed.txt")
DEFAULT_INPUT_FOLDER = Path("input_files")


# ----------------------------
# CASE NORMALIZATION (from HW 3/4)
# ----------------------------

def normalize_case(text: str) -> str:
    """Normalize case: capitalize sentence starts, lower the rest."""
    result, capitalize_next = "", True
    for ch in text:
        if capitalize_next and ch.isalpha():
            result += ch.upper()
            capitalize_next = False
        else:
            result += ch.lower()
        if ch in ".!?":
            capitalize_next = True
    return result


# ----------------------------
# RECORD PUBLISHERS (from HW 5)
# ----------------------------

def append_to_file(record: str):
    """Append a formatted record to the output file."""
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(record + "\n" + "-" * 40 + "\n")


def format_news(text: str, city: str) -> str:
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"NEWS -------------------------\n{normalize_case(text)}\nCity: {city}, {date}"


def format_private_ad(text: str, expiration_date: str) -> str:
    try:
        exp_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
        days_left = (exp_date - datetime.date.today()).days
        days_left_text = f"{days_left} days left" if days_left >= 0 else "Expired!"
    except ValueError:
        days_left_text = "Invalid date format"
    return f"PRIVATE AD -------------------\n{normalize_case(text)}\nExpires: {expiration_date} ({days_left_text})"


def format_quote(quote: str, author: str) -> str:
    weekday = datetime.datetime.now().strftime("%A")
    return f"QUOTE OF THE DAY ------------\n\"{normalize_case(quote)}\"\n— {normalize_case(author)}, shared on {weekday}"


# ----------------------------
# NEW CLASS FOR FILE INPUT
# ----------------------------

class FileInputProcessor:
    """
    Processes records from a file.
    Expected format per record:
    <TYPE>::<field1>::<field2>
    
    Example:
    NEWS::Python 3.13 released!::London
    AD::Selling my bike::2025-09-20
    QUOTE::Code is like humor. When you have to explain it, it’s bad.::Cory House
    """

    def __init__(self, file_path: Path = None):
        self.file_path = file_path or self.get_default_file()

    def get_default_file(self) -> Path:
        """Return first file in default folder, if available."""
        if not DEFAULT_INPUT_FOLDER.exists():
            DEFAULT_INPUT_FOLDER.mkdir()
        files = list(DEFAULT_INPUT_FOLDER.glob("*.txt"))
        return files[0] if files else None

    def process_file(self):
        if not self.file_path or not self.file_path.exists():
            print("❌ No input file found.")
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        for line in lines:
            parts = line.split("::")
            if len(parts) < 2:
                print(f"⚠️ Skipping malformed line: {line}")
                continue

            record_type = parts[0].upper()
            if record_type == "NEWS" and len(parts) == 3:
                append_to_file(format_news(parts[1], parts[2]))
            elif record_type == "AD" and len(parts) == 3:
                append_to_file(format_private_ad(parts[1], parts[2]))
            elif record_type == "QUOTE" and len(parts) == 3:
                append_to_file(format_quote(parts[1], parts[2]))
            else:
                print(f"⚠️ Unknown or malformed record: {line}")

        # Remove file after successful processing
        os.remove(self.file_path)
        print(f"✅ Processed and removed file: {self.file_path}")


# ----------------------------
# MAIN PROGRAM
# ----------------------------

def show_menu():
    while True:
        print("\n=== USER NEWS FEED ===")
        print("1. Publish News (manual)")
        print("2. Publish Private Ad (manual)")
        print("3. Publish Motivational Quote (manual)")
        print("4. Process from Input File")
        print("5. Exit")
        choice = input("Choose option (1-5): ")

        if choice == "1":
            append_to_file(format_news(input("Enter news text: "), input("Enter city: ")))
        elif choice == "2":
            append_to_file(format_private_ad(input("Enter ad text: "), input("Enter expiration date (YYYY-MM-DD): ")))
        elif choice == "3":
            append_to_file(format_quote(input("Enter quote: "), input("Enter author: ")))
        elif choice == "4":
            processor = FileInputProcessor()
            processor.process_file()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    show_menu()
