# Imports data from a CSV spreadsheet, For each student in the CSV file, insert the student into the students table in the students.db database
import csv
import cs50
from sys import argv, exit

db = cs50.SQL("sqlite:///students.db")

if len(argv) != 2:
    print("Incorrect number of command-line arguments")
    exit(1)

# Read database into memory
csv_file = open(argv[1])
new_file = csv.DictReader(csv_file)

for row in new_file:
    full_name = row['name'].split()
    if len(full_name) == 2:
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", full_name[0], None, full_name[1], row['house'], row['birth'])
    elif len(full_name) == 3:
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", full_name[0], full_name[1], full_name[2], row['house'], row['birth'])