import datetime
import csv
import os
import re
import json
import sqlite3
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


OUTPUT_FILE = Path("news_feed.txt")
DEFAULT_INPUT_FOLDER = Path("input_files")
WORD_COUNT_CSV = Path("word_count.csv")
LETTER_STATS_CSV = Path("letter_stats.csv")
DB_FILE = Path("news_feed.db")


# ----------------------------
# DATABASE MANAGER
# ----------------------------

class DatabaseManager:
    """Manages SQLite database tables and inserts records without duplicates."""

    def __init__(self, db_path=DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    city TEXT,
                    date TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS ads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    expiration_date TEXT,
                    days_left INTEGER
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quote TEXT NOT NULL,
                    author TEXT,
                    weekday TEXT
                )
            """)

    def insert_news(self, text, city, date):
        if not self._exists("news", "text=? AND city=? AND date=?", (text, city, date)):
            with self.conn:
                self.conn.execute(
                    "INSERT INTO news (text, city, date) VALUES (?, ?, ?)",
                    (text, city, date)
                )

    def insert_ad(self, text, expiration_date, days_left):
        if not self._exists("ads", "text=? AND expiration_date=?", (text, expiration_date)):
            with self.conn:
                self.conn.execute(
                    "INSERT INTO ads (text, expiration_date, days_left) VALUES (?, ?, ?)",
                    (text, expiration_date, days_left)
                )

    def insert_quote(self, quote, author, weekday):
        if not self._exists("quotes", "quote=? AND author=?", (quote, author)):
            with self.conn:
                self.conn.execute(
                    "INSERT INTO quotes (quote, author, weekday) VALUES (?, ?, ?)",
                    (quote, author, weekday)
                )

    def _exists(self, table, condition, params):
        cur = self.conn.cursor()
        cur.execute(f"SELECT 1 FROM {table} WHERE {condition} LIMIT 1", params)
        return cur.fetchone() is not None


db = DatabaseManager()  # Global database instance


# ----------------------------
# CASE NORMALIZATION
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
# RECORD FORMATTERS
# ----------------------------

def append_to_file(record: str):
    """Append a formatted record to the output file and regenerate statistics."""
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(record + "\n" + "-" * 40 + "\n")
    recreate_statistics()


def format_news(text: str, city: str) -> str:
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    db.insert_news(normalize_case(text), city, date)
    return f"NEWS -------------------------\n{normalize_case(text)}\nCity: {city}, {date}"


def format_private_ad(text: str, expiration_date: str) -> str:
    try:
        exp_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
        days_left = (exp_date - datetime.date.today()).days
        days_left_text = f"{days_left} days left" if days_left >= 0 else "Expired!"
    except ValueError:
        days_left, days_left_text = None, "Invalid date format"

    db.insert_ad(normalize_case(text), expiration_date, days_left)
    return f"PRIVATE AD -------------------\n{normalize_case(text)}\nExpires: {expiration_date} ({days_left_text})"


def format_quote(quote: str, author: str) -> str:
    weekday = datetime.datetime.now().strftime("%A")
    db.insert_quote(normalize_case(quote), normalize_case(author), weekday)
    return f"QUOTE OF THE DAY ------------\n\"{normalize_case(quote)}\"\n— {normalize_case(author)}, shared on {weekday}"


# ----------------------------
# FILE INPUT PROCESSORS
# ----------------------------

class FileInputProcessor:
    """Processes records from TXT file, using <TYPE>::<field1>::<field2> format."""

    def __init__(self, file_path: Path = None):
        self.file_path = file_path or self.get_default_file()

    def get_default_file(self) -> Path:
        if not DEFAULT_INPUT_FOLDER.exists():
            DEFAULT_INPUT_FOLDER.mkdir()
        files = list(DEFAULT_INPUT_FOLDER.glob("*.txt"))
        return files[0] if files else None

    def process_file(self):
        if not self.file_path or not self.file_path.exists():
            print("❌ No TXT input file found.")
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

        os.remove(self.file_path)
        print(f"✅ Processed and removed file: {self.file_path}")


class JSONInputProcessor:
    """Processes records from JSON file with a list of objects."""

    def __init__(self, file_path: Path = None):
        self.file_path = file_path or self.get_default_file()

    def get_default_file(self) -> Path:
        if not DEFAULT_INPUT_FOLDER.exists():
            DEFAULT_INPUT_FOLDER.mkdir()
        files = list(DEFAULT_INPUT_FOLDER.glob("*.json"))
        return files[0] if files else None

    def process_file(self):
        if not self.file_path or not self.file_path.exists():
            print("❌ No JSON input file found.")
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"❌ Failed to parse JSON: {self.file_path}")
                return

        records = data if isinstance(data, list) else [data]

        for record in records:
            rtype = record.get("type", "").upper()
            if rtype == "NEWS" and "text" in record and "city" in record:
                append_to_file(format_news(record["text"], record["city"]))
            elif rtype == "AD" and "text" in record and "expiration_date" in record:
                append_to_file(format_private_ad(record["text"], record["expiration_date"]))
            elif rtype == "QUOTE" and "quote" in record and "author" in record:
                append_to_file(format_quote(record["quote"], record["author"]))
            else:
                print(f"⚠️ Skipping malformed record: {record}")

        os.remove(self.file_path)
        print(f"✅ Processed and removed file: {self.file_path}")


class XMLInputProcessor:
    """Processes records from XML file with <record> nodes."""

    def __init__(self, file_path: Path = None):
        self.file_path = file_path or self.get_default_file()

    def get_default_file(self) -> Path:
        if not DEFAULT_INPUT_FOLDER.exists():
            DEFAULT_INPUT_FOLDER.mkdir()
        files = list(DEFAULT_INPUT_FOLDER.glob("*.xml"))
        return files[0] if files else None

    def process_file(self):
        if not self.file_path or not self.file_path.exists():
            print("❌ No XML input file found.")
            return

        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
        except ET.ParseError:
            print(f"❌ Failed to parse XML: {self.file_path}")
            return

        for rec in root.findall("record"):
            rtype = (rec.findtext("type") or "").upper()
            if rtype == "NEWS":
                text, city = rec.findtext("text"), rec.findtext("city")
                if text and city:
                    append_to_file(format_news(text, city))
            elif rtype == "AD":
                text, exp = rec.findtext("text"), rec.findtext("expiration_date")
                if text and exp:
                    append_to_file(format_private_ad(text, exp))
            elif rtype == "QUOTE":
                quote, author = rec.findtext("quote"), rec.findtext("author")
                if quote and author:
                    append_to_file(format_quote(quote, author))
            else:
                print(f"⚠️ Skipping malformed record: {ET.tostring(rec, encoding='unicode')}")

        os.remove(self.file_path)
        print(f"✅ Processed and removed file: {self.file_path}")


# ----------------------------
# CSV STATISTICS
# ----------------------------

def recreate_statistics():
    if not OUTPUT_FILE.exists():
        return

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    words = re.findall(r"\b\w+\b", text.lower())
    word_counts = Counter(words)
    with open(WORD_COUNT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        for word, count in sorted(word_counts.items()):
            writer.writerow([word, count])

    letters_only = [ch for ch in text if ch.isalpha()]
    total_counts = Counter(ch.lower() for ch in letters_only)
    upper_counts = Counter(ch.lower() for ch in text if ch.isupper())
    with open(LETTER_STATS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["letter", "count_all", "count_uppercase", "percentage"])
        for letter in sorted(total_counts.keys()):
            count_all = total_counts[letter]
            count_upper = upper_counts.get(letter, 0)
            percentage = round(count_upper / count_all * 100, 2) if count_all > 0 else 0
            writer.writerow([letter, count_all, count_upper, percentage])


# ----------------------------
# MAIN MENU
# ----------------------------

def show_menu():
    while True:
        print("\n=== USER NEWS FEED ===")
        print("1. Publish News (manual)")
        print("2. Publish Private Ad (manual)")
        print("3. Publish Motivational Quote (manual)")
        print("4. Process from TXT File")
        print("5. Process from JSON File")
        print("6. Process from XML File")
        print("7. Exit")
        choice = input("Choose option (1-7): ")

        if choice == "1":
            append_to_file(format_news(input("Enter news text: "), input("Enter city: ")))
        elif choice == "2":
            append_to_file(format_private_ad(input("Enter ad text: "), input("Enter expiration date (YYYY-MM-DD): ")))
        elif choice == "3":
            append_to_file(format_quote(input("Enter quote: "), input("Enter author: ")))
        elif choice == "4":
            FileInputProcessor().process_file()
        elif choice == "5":
            JSONInputProcessor().process_file()
        elif choice == "6":
            XMLInputProcessor().process_file()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    show_menu()
