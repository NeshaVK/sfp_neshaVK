import random

# Lists for codename parts
adjectives = ['Fearless', 'Brave', 'Clever', 'Mighty', 'Swift']
nouns = ['Dragon', 'Tiger', 'Phoenix', 'Wolf', 'Eagle']

# Ask user for their name
name = input("What is your name?\n")

# Generate random codename
codename = random.choice(adjectives) + " " + random.choice(nouns)

# Generate random lucky number
lucky_number = random.randint(1, 100)

# Print the results
print(f"{name}, your codename is: {codename}")
print(f"Your lucky number is: {lucky_number}")
