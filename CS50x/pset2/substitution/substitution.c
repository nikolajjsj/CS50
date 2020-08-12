#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // write to check for arguments and the correctness
    if (argc == 2 && strlen(argv[1]) == 26)
    {
        string key = argv[1];
        int key_length = strlen(key);
        // check key = argv[1]:
        for (int i = 0; i < key_length; i++)
        {
            for (int j = i + 1; j < key_length; j++)
            {
                if (key[i] == key[j] || !isalpha(key[i]))
                {
                    printf("Key is invalid\n");
                    return 1;
                }
            }
        }
        printf("Sucess\n");
    }
    else
    {
        printf("INVALID\n");
        return 1;
    }
    // key and key length
    string key = argv[1];
    int key_length = strlen(key);
    // prompt the user for a string, for ciphering
    string plain_text = get_string("plaintext: ");
    // cipher_text variable
    string cipher_text = malloc(strlen(plain_text));
    // array of alphabet:
    string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    // for loop going through the alphabet comparing to the plain_text retrieving the key value at same place
    for (int i = 0, plain_text_length = strlen(plain_text); i < plain_text_length; i++)
    {
        for (int j = 0; j < key_length; j++)
        {
            if (isupper(plain_text[i]))
            {
                if (plain_text[i] == toupper(alphabet[j]))
                {
                    cipher_text[i] = toupper(key[j]);
                }
            }
            else if (islower(plain_text[i]))
            {
                if (plain_text[i] == tolower(alphabet[j]))
                {
                    cipher_text[i] = tolower(key[j]);
                }
            }
            else
            {
                cipher_text[i] = plain_text[i];
            }
        }
    }

    // TODO: output "ciphertext: ", program must maintain upper- and lowerness, and finally return 0 from main!
    printf("ciphertext: %s\n", cipher_text);
    free(cipher_text);
    return 0;
}