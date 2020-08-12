from sys import argv, exit
import cs50

# open that database file for sqlite
db = cs50.SQL("sqlite:///students.db")

def main():
    # accept a argv length of 2: python import.py csv.csv
    if len(argv) != 2:
        print("Correct input: python import.py house")
        exit(1)

    # store the value written at command line, as the house to search students for
    house = argv[1]

    # execute sqlite code to get the students in said house
    studentList = db.execute("SELECT first, middle, last, birth FROM students WHERE house=(?) ORDER BY last, first", house)

    for dicts in studentList:
        # get correct name
        if dicts['middle'] == None:
            name = dicts['first'] + ' ' + dicts['last'] + ', '
        else:
            name = dicts['first'] + ' ' + dicts['middle'] + ' ' + dicts['last'] + ', '

        # retrieve birthdate
        birthdate = 'born ' + str(dicts['birth'])

        print(name + birthdate)


main()
