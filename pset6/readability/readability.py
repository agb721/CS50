# Uses Coleman-Liau formula to compute the approximate grade level needed to comprehend some text.

from cs50 import get_string

# Prompt for text
text = get_string("Text: ")

# Counter variables
letters = 0
words = 1 # not ideal for edge case of 0 sentences
sentences = 0

for c in text:
    #print(f"{c}")
    if c.isalpha():
        letters += 1
    if c == (" "):
        words += 1
    if c == (".") or c == ("!") or c == ("?"): # inefficient syntax here
        sentences += 1

# Calculates Coleman-Liau Index rounded to nearest integer
index = round(0.0588 * letters/(words/100) - 0.296 * sentences/(words/100) - 15.8)

if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")

