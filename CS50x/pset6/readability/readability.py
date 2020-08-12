from cs50 import get_string


def main():
    # loop until length of string > 0
    while True:
        string = get_string("Text: ")
        if len(string) > 0:
            break

    index = calculate_colemanliau(string)
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


# count letters function
def countletters(string):
    nletters = 0
    for letter in string:
        if letter.isalpha():
            nletters += 1
    return nletters


# count words function
def countwords(string):
    nwords = 0
    for char in string:
        if char is " ":
            nwords += 1
    return nwords + 1


# count sentences function
def countsentences(string):
    nsentences = 0
    for char in string:
        if char in [".", "!", "?"]:
            nsentences += 1
    return nsentences


# and finally function to calculate the index from the Coleman-Liau formula:
# 0.0588 * L - 0.296 * S - 15.8
# L = average number of letters per 100 words
# S average number of sentences per 100 words
def calculate_colemanliau(string):
    L = (100 / countwords(string)) * countletters(string)
    S = (100 / countwords(string)) * countsentences(string)
    return round(0.0588 * L - 0.296 * S - 15.8)


main()
