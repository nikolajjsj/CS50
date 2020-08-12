#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;
            float average_float = (float)(red + green + blue) / 3;
            int average = round(average_float);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, half_width = width / 2; j < half_width; j++)
        {
            // switch the individual RGBTRIPLE's from 0 and i - j, until the middle
            RGBTRIPLE tmp = image[i][j];
            // the start should now equal the end triplet
            image[i][j] = image[i][width - (j + 1)];
            // and end should be equal to start/tmp
            image[i][width - (j + 1)] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // create an array and copy the image
    RGBTRIPLE image_copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image_copy[i][j] = image[i][j];
        }
    }

    // variables for the rgb channels sums, and a counter variable
    int r_sum, g_sum, b_sum, neighbour_triplets = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // blur one triplet by averaging over all the touching triplets
            r_sum = 0;
            g_sum = 0;
            b_sum = 0;

            // neighbour_triplets counts number of neighbouring triplets
            neighbour_triplets = 0;

            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    if (i + x >= 0 && i + x < height && j + y >= 0 && j + y < width)
                    {
                        r_sum += image_copy[i + x][j + y].rgbtRed;
                        g_sum += image_copy[i + x][j + y].rgbtGreen;
                        b_sum += image_copy[i + x][j + y].rgbtBlue;
                        neighbour_triplets++;
                    }
                }
            }
            image[i][j].rgbtRed = round(r_sum / (float) neighbour_triplets);
            image[i][j].rgbtGreen = round(g_sum / (float) neighbour_triplets);
            image[i][j].rgbtBlue = round(b_sum / (float) neighbour_triplets);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // first make a copy of the image for the original colors:
    RGBTRIPLE image_copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image_copy[i][j] = image[i][j];
        }
    }

    // make an array to form the Gx method
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};


    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // edge detect through Gx method from walkthrough
            // and here are the triplets with 8 touching tiplets
            int r_gx = 0;
            int r_gy = 0;
            int g_gx = 0;
            int g_gy = 0;
            int b_gx = 0;
            int b_gy = 0;

            // loop utilizing the Gx, Gy arrays and the surrounding pixels of the calculated pixel
            for (int x = 0; x < 3; x++)
            {
                for (int y = 0; y < 3; y++)
                {
                    // out of bounds pixels
                    if (i - 1 + x < 0 || i - 1 + x >= height || j - 1 + y < 0 || j - 1 + y >= width)
                    {
                        continue;
                    }

                    // Gx calculations
                    r_gx += image_copy[i - 1 + x][j - 1 + y].rgbtRed * gx[x][y];
                    g_gx += image_copy[i - 1 + x][j - 1 + y].rgbtGreen * gx[x][y];
                    b_gx += image_copy[i - 1 + x][j - 1 + y].rgbtBlue * gx[x][y];

                    // Gy calculations
                    r_gy += image_copy[i - 1 + x][j - 1 + y].rgbtRed * gy[x][y];
                    g_gy += image_copy[i - 1 + x][j - 1 + y].rgbtGreen * gy[x][y];
                    b_gy += image_copy[i - 1 + x][j - 1 + y].rgbtBlue * gy[x][y];
                }
            }
            // resulting rgb channels
            int result_red = round(sqrt((float) (r_gx * r_gx) + (r_gy * r_gy)));
            int result_green = round(sqrt((float) (g_gx * g_gx) + (g_gy * g_gy)));
            int result_blue = round(sqrt((float) (b_gx * b_gx) + (b_gy * b_gy)));

            // using ternery operator to check for values over 255
            image[i][j].rgbtRed = (result_red > 255) ? 255 : result_red;
            image[i][j].rgbtGreen = (result_green > 255) ? 255 : result_green;
            image[i][j].rgbtBlue = (result_blue > 255) ? 255 : result_blue;
        }
    }
    return;
}
