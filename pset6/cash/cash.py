# Returns minimum number of coins needed to return cash of a certain inputted amount

from cs50 import get_float
from time import sleep


# Request info for cash change amount and repromt if negative
cash = -1
while cash < 0:
    cash = get_float("How much? ")

# Convert and round cash in dollar to cents
cents = round(cash*100, 2)

# Counter variable
counter = 0

# Count quarters
while cents >= 25:
    counter += 1
    cents -= 25

# Count dimes
while cents >= 10:
    counter += 1
    cents -= 10
    
# Count nickles
while cents >= 5:
    counter += 1
    cents -= 5

# Count pennies
while cents >= 1:
    counter += 1
    cents -= 1

# Number of coins use
print(f"{counter}")