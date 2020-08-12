#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>

// definitions
#define BUFFERSIZE 512
typedef uint8_t BYTE;

// functions:
bool checkForJpeg(BYTE buffer[]);

int main(int argc, char *argv[])
{
    // check for the right number of comand line arguments, if not return 1
    if (argc != 2)
    {
        printf("Remember to add one, and only one, command to the program execution!\n");
        return 1;
    }

    // open the file given in the comand line
    char *input = argv[1];
    FILE *file = fopen(input, "r");

    // if this file equals: NULL, then return 1
    if (file == NULL)
    {
        printf("File: %s, could not be opened...\n", input);
        return 1;
    }

    // variables for looping through the memorycard file
    BYTE buffer[BUFFERSIZE];
    int n_jpeg = 0;
    FILE *jpeg_image = NULL;
    char file_name [8];

    // looping through the file
    while (!feof(file) && fread(&buffer, BUFFERSIZE, 1, file) == true)
    {
        // identify start of a jpeg file, with defined function
        if (checkForJpeg(buffer))
        {
            // if first found jpeg image
            if (n_jpeg == 0)
            {
                // initiate a new file for found jpeg image
                sprintf(file_name, "%03i.jpg", n_jpeg);
                jpeg_image = fopen(file_name, "w");
                fwrite(buffer, 1, BUFFERSIZE, jpeg_image);
                n_jpeg++;
            }
            // if already found a jpeg image
            else
            {
                // close the current jpeg file
                fclose(jpeg_image);

                // and start a new jpeg image file
                sprintf(file_name, "%03i.jpg", n_jpeg);
                jpeg_image = fopen(file_name, "w");
                fwrite(buffer, 1, BUFFERSIZE, jpeg_image);
                n_jpeg++;
            }
        }

        // no new jpeg found
        else if (!checkForJpeg(buffer))
        {
            // just continue to the next buffer if no jpeg has been found yet
            if (n_jpeg == 0)
            {
                continue;
            }
            else
            {
                fwrite(buffer, 1, BUFFERSIZE, jpeg_image);
            }
        }
    }

    // if end of file stream close of the program and return 0, all is good :)
    if (feof(file))
    {
        fclose(file);
    }

    // and return 0;
    return 0;
}

bool checkForJpeg(BYTE buffer[])
{
    return (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0);
}
