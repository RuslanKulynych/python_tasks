# Import the random module to generate random numbers
import random

# Generate a list of 100 random integers between 0 and 1000
random_numbers = [random.randint(0, 1000) for _ in range(100)]

# Create a copy of the original list to sort it
sorted_numbers = random_numbers.copy()

# Implement selection sort manually (without using a function)
# Outer loop to iterate through the list
for i in range(len(sorted_numbers)):
    # Assume the current index is the smallest
    min_index = i
    # Inner loop to find the smallest element in the remaining unsorted list
    for j in range(i + 1, len(sorted_numbers)):
        # Compare and update the index of the smallest value
        if sorted_numbers[j] < sorted_numbers[min_index]:
            min_index = j
    # Swap the found smallest element with the element at the current position
    sorted_numbers[i], sorted_numbers[min_index] = sorted_numbers[min_index], sorted_numbers[i]

# Initialize variables to store the sum and count of even numbers
even_sum = 0
even_count = 0

# Initialize variables to store the sum and count of odd numbers
odd_sum = 0
odd_count = 0

# Loop through the sorted list to process each number
for number in sorted_numbers:
    # Check if the number is even
    if number % 2 == 0:
        # Add the even number to even_sum
        even_sum += number
        # Increment the even_count
        even_count += 1
    else:
        # Add the odd number to odd_sum
        odd_sum += number
        # Increment the odd_count
        odd_count += 1

# Calculate the average of even numbers; avoid division by zero
if even_count != 0:
    even_average = even_sum / even_count
else:
    even_average = 0

# Calculate the average of odd numbers; avoid division by zero
if odd_count != 0:
    odd_average = odd_sum / odd_count
else:
    odd_average = 0

# Print the average of even numbers
print("Average of even numbers:", even_average)

# Print the average of odd numbers
print("Average of odd numbers:", odd_average)
