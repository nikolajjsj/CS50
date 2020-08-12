from sys import argv, exit
import csv

def main():
    if len(argv) != 3:
        print("Wrong command format, right: dna.py command1 command2")
        exit(1)
    # list of str's
    strs = []
    # persons str occurences
    names = []
    str_occurences = []
    # open csv file
    with open(argv[1], "r") as csvfile:
        # reader of csv file
        reader = csv.reader(csvfile)
        # loop over csv file getting all the str's
        for row in reader:
            if row[0] == "name":
                strs.extend(row[1:len(row)])
            else:
                names.append(row[0])
                tmp = row[1:len(row)]
                occurs = []
                for i in tmp:
                    occurs.append(int(i))
                str_occurences.append(occurs)

        # read text file
        with open(argv[2], "r") as textfile:
            text = textfile.read()
            # number of each target occurences
            occurences = consecutive_occurences(strs, text)
            # now find which row/person equals the target occurences
            for i in range(len(names)):
                if str_occurences[i] == occurences:
                    print(names[i])
                    exit(1)


    print("No match")
    exit(0)


def consecutive_occurences(array, text):
    # array for occurences of specific target
    occurs = []

    #looping through each target DNA
    for target in array:
        index_array = [0] * len(text)
        for i in range(len(text) - len(target), -1, -1):
            if text[i: i + len(target)] == target:
                if i + len(target) > len(text) - 1:
                    index_array[i]
                else:
                    index_array[i] += index_array[i + len(target)] + 1
        occurs.append(max(index_array))
    return occurs


main()