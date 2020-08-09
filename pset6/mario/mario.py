# CS50 Prints pyramid of height provided by the user. Previously wrote this program in C.
# This serves a exercise to get used to Python syntax
# Instrucitons: https://cs50.harvard.edu/x/2020/psets/6/

from cs50 import get_int
from sys import argv, exit


def main():
    # Prompt user for height
    height = get_height()
    # This loop prints the pyramid height
    for i in range(height):
        # This loop print the spaces in a row
        for j in range(height-(i+1)):
            print(" ", end="")
        # Prints pund signs in a row
        for z in range(i):
            print("#", end="")
        print("#")


def get_height():
    while True:
        height = get_int("Height: ")
        if height >= 1 and height <= 8:
            break
    return height


main()