from cs50 import get_int, get_string
from sys import argv

def main():
    # credit card number
    number = get_int("Number: ")
    # length of credit card number
    length = len(str(number))

    if checkCardValidity(number):
        if length == 15 and int(str(number)[:2]) in [34, 37]:
            print("AMEX")
        elif length == 13 and int(str(number)[:1]) == 4:
            print("VISA")
        elif length == 16:
            if int(str(number)[:2]) in [51, 52, 53, 54, 55]:
                print("MASTERCARD")
            elif int(str(number)[:1]) == 4:
                print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")

def checkCardValidity(number):
    # check for validity through Luhn’s algorithm
    sum1 = 0;
    sum2 = 0;
    # calculate sum1 and 2
    for i,x in enumerate(reversed(str(number))):
        n = int(x)
        if i % 2 == 0:
            sum2 += n
        else:
            n = n * 2
            sum1 += sum([int(n) for n in str(n)])
    # sum
    final_sum = sum1 + sum2
    # if last digit is 0 return True
    if str(final_sum).endswith("0"):
        return True
    else:
        return False

main()