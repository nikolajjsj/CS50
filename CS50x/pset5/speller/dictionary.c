// Implements a dictionary's functionality
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 20000;

// Hash table
node *table[N];

// variable to store number of words in the dictionary
int dict_size = 0;



// 4. Returns true if word is in dictionary else false, should not care about capitalization
bool check(const char *word)
{
    // copy word
    char copy[LENGTH + 1];
    // for loop to go through the word making all char lowercase
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        copy[i] = tolower(word[i]);
    }

    // then add null terminator to the end of the word
    copy[strlen(word)] = '\0';

    // get the index of the word by hashing
    int index = hash(copy);

    // set node to point to the hashtable by index
    node *pointer = table[index];

    // iterate over the linked list at this place in the hastable to check for word
    while (pointer != NULL)
    {
        if (strcasecmp(pointer->word, copy) == 0)
        {
            return true;
        }
        else
        {
            pointer = pointer->next;
        }
    }
    // if the pointer reaches the end of the hash tables linked list return false
    return false;
}

// 2. Hashes word to a number, from Reddit CS50: u/delipity
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash = (hash << 2) ^ word[i];
    }
    return hash % N;
}

// 1. Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Remember to free any allocated memory
    // open dictionary file
    FILE *file = fopen(dictionary, "r");

    // check if file was loaded correctly
    if (file == NULL)
    {
        return false;
    }

    // string (char *) for each word
    char word[LENGTH + 1];

    // while loop utilizing fscanf, to loop through each word
    while (fscanf(file, "%s", word) != EOF)
    {
        // create a new node for each word
        node *n = malloc(sizeof(node));

        // check for correctly allocated memory
        if (n == NULL)
        {
            free(n);
            return false;
        }

        // using strcopy to copy word from file into node
        strcpy(n->word, word);

        // hash word to obtain hash value
        int index = hash(word);

        // then put word into hashtable
        n->next = table[index];
        table[index] = n;
        dict_size++;
    }
    fclose(file);
    return true;
}

// 3. Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return dict_size;
}

// 5. Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node* pointer = table[i];
        while (pointer != NULL)
        {
            node* tmp = pointer;
            pointer = pointer->next;
            free(tmp);
        }
        free(pointer);
    }
    return true;
}
