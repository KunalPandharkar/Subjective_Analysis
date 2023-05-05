import re

# Define the regex pattern to match roll numbers
pattern = r'BE\d{2}S\d{2}F\d{3}'

# Example string containing roll numbers
string = 'These are some roll numbers: BE20S06F010, BE20S06F011, BE20S06F012'

# Find all roll numbers in the string using regex
roll_numbers = re.findall(pattern, string)

# Print out the roll numbers
print(roll_numbers)
