#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;

    // do while loop to keep retrieving a number from the user unless the number is 1-8
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // printing the tree, first getting the number of rows
    for (int i = 1; i <= height; i++)
    {
        // then printing the spaces
        for (int j = 0; j < height - i; j++)
        {
            printf(" ");
        }

        // then printing the number of hashes for the first part of the tree
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }

        // printing the spaces between the two parts
        printf("  ");

        //then printing the other side of the tree
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }

        // and finally going to the next line
        printf("\n");
    }
}