#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int get_letters();
int get_words();
int get_sentences();
void calculation();

int main(void)
{
    // prompt user for a string/text:
    string text = get_string("Text: ");

    // get length of string
    int text_length = get_letters(text);

    // get number of words
    int text_words = get_words(text);

    // get number of sentences
    int text_sentences = get_sentences(text);

    // calculate the index
    calculation(text_words, text_length, text_sentences);
}

int get_letters(string input)
{
    // letter is any lowercase or uppercase character
    int text_length = strlen(input);
    int number_letters = 0;
    for (int i = 0; i < text_length; i++)
    {
        if (isalnum(input[i]))
        {
            number_letters++;
        }
    }
    return number_letters;
}

int get_words(string input)
{
    // letter is any lowercase or uppercase character
    int text_length = strlen(input);
    int n_words = 0;
    for (int i = 0; i < text_length; i++)
    {
        if (input[i] == ' ')
        {
            n_words++;
        }
    }
    return n_words + 1;
}

int get_sentences(string input)
{
    // sentences is any strings seperated by: ! . ?
    int text_length = strlen(input);
    int n_sentences = 0;
    for (int i = 0; i < text_length; i++)
    {
        if (input[i] == '!' || input[i] == '.' || input[i] == '?')
        {
            n_sentences++;
        }
    }
    return n_sentences;
}

void calculation(int words, int letters, int sentences)
{
    // calculates via the formula: index = 0.0588 * L - 0.296 * S - 15.8
    // L = average number of letters per 100 words
    // S = average number of sentences per 100 words
    double L = (100.0 / words) * letters;
    double S = (100.0 / words) * sentences;

    double index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = round(index);

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %d\n", grade);
    }
}