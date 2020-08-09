#  Identifies a person based on their DNA.
from sys import argv, exit
import csv
import re


def main():

    # Check for proper usage
    if len(argv) != 3:
        print("Missing command-line argument")
        exit(1)

    # Read database into memory
    database_file = open(argv[1])
    database = csv.reader(database_file)

    rows = []
    for row in database:
        rows.append(row)

    # Load STR names into list
    STRs = rows[0]
    STRs.pop(0)
    ##print(STRs)

    # Load DNA sequence into string
    sequence_file = open(argv[2])
    seq = sequence_file.read()

    # List to insert each maximum STR count
    reps_list = [[] for x in range(len(STRs))]
    max_reps_list = []
    ##print(f"reps_list {reps_list}")

    for x in range(len(STRs)): # Do for each STR
      STR = STRs[x]
      for i in range(len(seq)): # Iterate through sequence looking for STR
          if seq[i:i+len(STR)] == STR: # Recognize STR
              reps_list[x].append(cons_STR(seq, STR, i)) # Count consequtive repetitions of STR
          else:
              i += 1

    # Add max values to max_reps_list
      if len(reps_list[x]) >= 1:
        max_reps_list.append(str(max(reps_list[x])))
    ##print(f"max_reps_list {max_reps_list}")

    check = []
    for i in range(1,len(rows)):
        check.append(rows[i][1:len(rows[i])])

    # Compare check with max_reps_list
    found = False
    for x in range(len(check)):
        if max_reps_list == check[x]:
            found = True
            print(rows[x+1][0])
    if found == False:
        print("No match")


def cons_STR(seq, STR, i = 0, nest = 0, reps = 0):
    if seq[i:i+len(STR)] != STR:
        reps = nest
        return reps
    else:
        reps = cons_STR(seq, STR, i+len(STR), nest+1, reps)
    return reps


main()