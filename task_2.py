import random  # Import random module for generating random numbers
import string  # Import string module to get letters

# Step 1: Generate a random number of dictionaries (between 2 and 10)
list_of_dicts = []  # This will hold all generated dictionaries
for _ in range(random.randint(2, 10)):  # Repeat 2-10 times
    dict_size = random.randint(1, 5)  # Random number of keys per dict (1-5)
    keys = random.sample(string.ascii_lowercase, dict_size)  # Get random unique letters
    new_dict = {}  # Create a new empty dictionary
    for k in keys:  # Fill dictionary with key-value pairs
        new_dict[k] = random.randint(0, 100)  # Random value between 0-100
    list_of_dicts.append(new_dict)  # Add dictionary to list

print("Generated list of dictionaries:", list_of_dicts)  # Show the generated data

# Step 2: Merge dictionaries into a single result dictionary
merged_dict = {}  # This will hold the final merged dictionary

# Iterate over all dictionaries with index to know which dict has the max value
for idx, d in enumerate(list_of_dicts):  # idx will be dictionary number (starting from 0)
    for key, value in d.items():  # Iterate over key-value pairs
        if key not in merged_dict:  # If key is not already in merged dict
            merged_dict[key] = (value, idx)  # Store value + index of dict where it came from
        else:  # If key already exists
            if value > merged_dict[key][0]:  # If current value is greater than stored value
                merged_dict[key] = (value, idx)  # Replace with max value + its dict index

# Build the final dictionary with renamed keys when needed
final_dict = {}
for key, (value, idx) in merged_dict.items():  # Unpack value and dict index
    count_key_occurrences = sum([key in d for d in list_of_dicts])  # Count how many dicts had this key
    if count_key_occurrences > 1:  # If key was present in more than one dict
        final_dict[f"{key}_{idx+1}"] = value  # Rename with dict number (1-based index)
    else:  # If key was unique
        final_dict[key] = value  # Keep original key name

print("Final merged dictionary:", final_dict)  # Show result
