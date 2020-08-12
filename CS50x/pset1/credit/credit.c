#include <stdio.h>
#include <cs50.h>

// Tasks //
// 1. Prompt for input
// 2. Calculate the checksum
// 3. Check for card length and starting digits
// 4. Print AMEX, MASTERCARD, VISA, or INVALID

int getCreditLength(long crednumb);
int calculateFirstSum(long crednumb);
int calculateSecondSum(long crednumb);
bool checkCardValidity(int sum);
int getTwoFirstDigits(long crednumb);
int getFirstDigit(long crednumb);

int main(void)
{
    long cred_nr;
    int cred_length;
    // prompt the user for the credit card number
    do
    {
        cred_nr = get_long("Number: ");
        cred_length = getCreditLength(cred_nr);
    }
    while (cred_length < 10 || cred_length == 14 || cred_length > 17);

    // get the sum of the calculation
    int sum = calculateFirstSum(cred_nr) + calculateSecondSum(cred_nr);

    if (checkCardValidity(sum))
    {
        int twoDigits = getTwoFirstDigits(cred_nr);
        if (getFirstDigit(cred_nr) == 4)
        {
            if (cred_length == 13 || cred_length == 16)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }

        }
        else if (twoDigits == 34 || twoDigits == 37)
        {
            printf("AMEX\n");
        }
        else if (twoDigits > 50 && twoDigits < 56)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}


// function to get the length of the creditcard number
int getCreditLength(long crednumb)
{
    long i = crednumb;
    int length = 0;
    while (i != 0)
    {
        length++;
        i = i / 10;
    }
    return length;
}

// function to calculate the first sum
int calculateFirstSum(long crednumb)
{
    // gets the credit card number
    long i = crednumb;

    // calculate the sum of every other character
    int first_sum = 0;
    i /= 10;
    if ((i % 10) * 2 > 9)
    {
        int x = (i % 10) * 2;
        do
        {
            first_sum = first_sum + (x % 10);
            x /= 10;
        }
        while (x);
    }
    else
    {
        first_sum = first_sum + ((i % 10) * 2);
    }
    do
    {
        i /= 10;
        i /= 10;
        int x = (i % 10) * 2;
        if (x > 9)
        {
            do
            {
                first_sum = first_sum + (x % 10);
                x /= 10;
            }
            while (x);
        }
        else
        {
            first_sum = first_sum + x;
        }

    }
    while (i);
    printf("First: %d\n", first_sum);
    return first_sum;
}

// function to calculate the second sum
int calculateSecondSum(long crednumb)
{
    // gets the credit card number
    long i = crednumb;

    // calculate the sum of every other character
    int second_sum = 0;
    second_sum = second_sum + (i % 10);
    do
    {
        i /= 10;
        i /= 10;
        second_sum = second_sum + (i % 10);
    }
    while (i);
    return second_sum;
}

bool checkCardValidity(int sum)
{
    if (sum % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

int getTwoFirstDigits(long crednumb)
{
    long i = crednumb;
    while (i >= 100)
    {
        i /= 10;
    }
    return i;
}

int getFirstDigit(long crednumb)
{
    long i = crednumb;
    while (i >= 10)
    {
        i /= 10;
    }
    return i;
}