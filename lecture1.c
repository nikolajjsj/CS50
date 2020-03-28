#include <stdio.h>

// First function to print: "Hello, World!", but stays on same line..
int main(void)
{
    printf('Hello, World!');
}

// to fix use this tag "/n"
int main(void)
{
    printf('Hellow, World!/n');
}

// for or while loop:
int main(void)
{
    int counter = 0;
    while( counter < 50 )
    {
        printf('Hello, World!');
        counter++;
    }

    for ( int i = 0; i < 50; i++ )
    {
        printf('i is still less than 50');
    }
}