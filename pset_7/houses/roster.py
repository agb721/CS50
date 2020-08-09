# Prints a list of students for a given house in alphabetical order
import csv
import cs50
from sys import argv, exit

if len(argv) != 2:
    print("Incorrect number of command-line arguments")
    exit(1)

db = cs50.SQL("sqlite:///students.db") 
house = argv[1]
query = db.execute("SELECT * FROM students WHERE house = ? ORDER BY last, first", house)
for row in query:
    if row['middle'] == None:
        print("{} {}, born {}".format(row['first'], row['last'], row['birth']))
    else:
        print("{} {} {}, born {}".format(row['first'], row['middle'], row['last'], row['birth']))
    