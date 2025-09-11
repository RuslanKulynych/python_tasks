# Step 1: Copy text to a variable as is (triple quotes preserve all whitespaces, including newlines)
text = """homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87. use no functions"""

# Step 2: Normalize letter cases → make first letter uppercase, rest lowercase, keep paragraph structure
normalized = ""  # We'll build normalized text here
capitalize_next = True  # Flag to know when to capitalize (start of sentence)

for ch in text:  # Go through each character
    if capitalize_next and ch.isalpha():  # If we should capitalize this letter
        normalized += ch.upper()
        capitalize_next = False
    else:
        normalized += ch.lower()  # Make everything else lowercase

    if ch in ".!?":  # If character ends a sentence
        capitalize_next = True  # Next letter must be capitalized

# Step 3: Fix "iz" only when it is a mistake (when " iz " as a word, not part of something else)
fixed = ""
i = 0
while i < len(normalized):
    if normalized[i:i+4] == " iz ":
        fixed += " is "  # Replace with correct "is"
        i += 4  # Skip over " iz "
    else:
        fixed += normalized[i]
        i += 1

# Step 4: Create extra sentence with LAST WORDS of each existing sentence
# We'll find last words by scanning text manually
last_words = []
word = ""
for i in range(len(fixed)):
    if fixed[i].isalpha():  # Build current word
        word += fixed[i]
    else:
        if word:  # If we have a complete word
            if fixed[i] in ".!?":  # If sentence ends here
                last_words.append(word)
            word = ""  # Reset word buffer

extra_sentence = " ".join(last_words).capitalize() + "."  # Join last words into one sentence

# Step 5: Add the new sentence to the end of the paragraph
final_text = fixed + " " + extra_sentence

# Step 6: Count all whitespace characters (spaces, tabs, newlines, etc.)
whitespace_count = 0
for ch in final_text:
    if ch.isspace():  # Count any kind of whitespace
        whitespace_count += 1

print("Normalized & Fixed Text:\n")
print(final_text)
print("\nNumber of whitespace characters:", whitespace_count)
