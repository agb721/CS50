#  Identifies a person based on their DNA.
from sys import argv, exit
import csv
import re

def main():
    if len(argv) != 3:
        print("Missing command-line argument")
        exit(1)
    
    # Read into memory
    people_file = open(argv[1], "r")
    dna_file = open(argv[2], "r")
    people = csv.reader(people_file)
    dna = dna_file.read()
    
    # Get columns in csv file using function below
    columns = variables(people)
    for i in range(len(columns)):
        print(f"This is variable number {i}: {columns[i]}")   
        
    # Look for exact matches in DNA Sequence person by person 
    # (how exactly does the csv reading work?: we're starting from the second line in the following loop) 
    # next(people)
    for row in people:
        match_counter = 0
        STRs = [0] * (len(row) - 1)
        for i in range(1,len(row)):
            STRs[i-1] = columns[i]*int(row[i])
        print(f"STRs are {STRs}")
        
        for i in [0,1,2]:
            if STRs[i] in dna:
                match_counter += 1
                
        if match_counter == len(row) - 1:
            print(row[0])
            exit (0)
    print("No match")
                
# Creates variables for each column in csv
def variables(n):
    for row in n:
        STRs = [0] * len(row)
        i = 0
        for value in range(len(row)):
            STRs[i] = row[value]
            print(STRs[i])
            i += 1
        break
    return STRs

main()

