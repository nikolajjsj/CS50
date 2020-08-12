from sys import argv, exit
import csv
import cs50

# open that database file for sqlite
db = cs50.SQL("sqlite:///students.db")

def main():
    # accept a argv length of 2: python import.py csv.csv
    if len(argv) != 2:
        print("Correct input: python import.py csv_file.csv")
        exit(1)

    with open(argv[1], "r") as csvfile:
        # reader to read the opened csv file
        reader = csv.DictReader(csvfile)

        # for loop to read the rows of the csv file
        for row in reader:
            # make a function that goes through the name and determines first, middle, last name
            # if no middle name then it should equal NULL
            # these names should be parsed into their respective columns in the database
            # array, using split() function to get a list of words in a string
            names = row['name'].split()
            # retrieve first, middle, and last name from the list, depending on the length
            if len(names) == 3:
                firstName = names[0]
                middleName = names[1]
                lastName = names[2]
            elif len(names) == 2:
                firstName = names[0]
                middleName = None
                lastName = names[1]
            # house and birth
            house = row['house']
            birth = row['birth']

            # now for writing these fields to the database, using the execute command
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", firstName, middleName, lastName, house, birth)



main()
