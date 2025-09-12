import random
import string
from collections import defaultdict, Counter
from pprint import pprint


# ----------------------------
# MODULE 2: Random Dict Merger
# ----------------------------

def generate_random_dicts(num_dicts=None, dict_size_range=(1, 5), value_range=(0, 100)):
    """Generate a list of random dictionaries."""
    num_dicts = num_dicts or random.randint(2, 10)
    return [
        {k: random.randint(*value_range) for k in random.sample(string.ascii_lowercase, random.randint(*dict_size_range))}
        for _ in range(num_dicts)
    ]


def merge_dicts_max(dicts):
    """Merge dictionaries by taking max value for duplicate keys."""
    merged = defaultdict(lambda: (-1, -1))
    for idx, d in enumerate(dicts):
        for k, v in d.items():
            if v > merged[k][0]:
                merged[k] = (v, idx)
    return merged


def build_final_dict(merged, dicts):
    """Build final dictionary with renamed keys if duplicates exist."""
    key_counts = Counter(k for d in dicts for k in d)
    final = {}
    for k, (v, idx) in merged.items():
        final_key = f"{k}_{idx+1}" if key_counts[k] > 1 else k
        final[final_key] = v
    return final


def module2_solution():
    """Run full solution for Module 2."""
    dicts = generate_random_dicts()
    pprint(dicts)
    merged = merge_dicts_max(dicts)
    final = build_final_dict(merged, dicts)
    pprint(final)
    return final


# ----------------------------
# MODULE 3: Text Normalizer
# ----------------------------

def normalize_case(text):
    """Capitalize first letter of each sentence, lower the rest."""
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


def fix_iz(text):
    """Replace 'iz' with 'is' only when it is a separate word."""
    result, i = "", 0
    while i < len(text):
        if (text[i:i+2].lower() == "iz" and
            (i == 0 or not text[i-1].isalpha()) and
            (i+2 == len(text) or not text[i+2].isalpha())):
            result += "is"
            i += 2
        else:
            result += text[i]
            i += 1
    return result


def extract_last_words(text):
    """Return list of last words from each sentence."""
    last_words, word = [], ""
    for i, ch in enumerate(text):
        if ch.isalpha():
            word += ch
        else:
            if word:
                if ch in ".!?":
                    last_words.append(word)
                word = ""
    if word:
        last_words.append(word)
    return last_words


def append_extra_sentence(text):
    """Append a sentence made from last words of each sentence."""
    last_words = extract_last_words(text)
    return text + " " + " ".join(last_words).capitalize() + "."


def count_whitespace(text):
    """Count all whitespace characters in the text."""
    return sum(ch.isspace() for ch in text)


def module3_solution(text):
    """Run full solution for Module 3."""
    normalized = normalize_case(text)
    fixed = fix_iz(normalized)
    final = append_extra_sentence(fixed)
    whitespaces = count_whitespace(final)
    print("\nNormalized & Fixed Text:\n")
    print(final)
    print("\nNumber of whitespace characters:", whitespaces)
    return final, whitespaces


# ----------------------------
# MAIN EXECUTION (for testing)
# ----------------------------

if __name__ == "__main__":
    print("\n=== MODULE 2 SOLUTION ===")
    module2_solution()

    print("\n=== MODULE 3 SOLUTION ===")
    text = """homEwork:
      tHis iz your homeWork, copy these Text to variable.

      You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

      it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

      last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87. use no functions"""
    module3_solution(text)
