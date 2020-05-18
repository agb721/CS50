// Resizes a BMP file ny factor of n

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    // name second and third arguments after 'infile' and 'outfile'. Is '*infile' a pointer's name or a pointer itself? Is there even a difference
    int n = atoi(argv[1]); // turns strings/pointers into numbers
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r"); // What is the difference between '*inptr' and '* infile'? Why is doesn't the infile' inside the fopen argument have a star?
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr); // why are we closing inptr here?
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    //READ
    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4; // Calculates padding in infile to later insert it in outfile (in copy program).

    // Look into bf and bi
    printf("bf.Size:%08x\n", bf.bfSize);
    printf("ImageWidth:%08x\n", bi.biWidth);
    //Declare new variable to store negative-sign Height in
    int new_imageHeight = abs(bi.biHeight);
    printf("ImageHeight:%08x\n", new_imageHeight);
    printf("ImageSize:%08x\n", bi.biSizeImage);
    printf("---------------\n");

    //CHECK
    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // UPDATE VARIABLES
    // New width, height, padding
    int new_width = bi.biWidth*n;
    int new_height = bi.biHeight*n;
    int new_padding = (4 - (new_width* sizeof(RGBTRIPLE)) % 4) % 4;

    // New header variables
    int new_SizeImage = (((new_width * sizeof(RGBTRIPLE)) + new_padding) * abs(new_height));
    int new_bfSize = (54 + new_SizeImage);

    // UPDATE HEADERS with Variables
    // Update BITMAPFILEHEADER
    BITMAPFILEHEADER new_bf = bf;
    new_bf.bfSize = new_bfSize;
    // Update BITMAPINFOHEADER
    BITMAPINFOHEADER new_bi = bi;
    new_bi.biSizeImage = new_SizeImage;
    new_bi.biWidth = new_width;
    new_bi.biHeight = new_height;

    printf("NEW.bf.Size:%08x\n", new_bf.bfSize);
    printf("NEW.ImageSize:%08x\n", new_bi.biSizeImage);
    printf("NEW.ImageWidth:%08x\n", new_bi.biWidth);
    printf("NEW.ImageHeight:%08x\n", new_bi.biHeight);
    printf("NEW.padding:%i\n", new_padding);


    //WRITE
    // write outfile's BITMAPFILEHEADER
    fwrite(&new_bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&new_bi, sizeof(BITMAPINFOHEADER), 1, outptr); // Probably both fwrite functions use the same cursor. That's how it starts writing one header after the other.

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        for (int p = 0; p < (n-1); p ++)
        {
             // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr); // reading cursor probably left off right after BITMAPINFOHEADER in infile.

                // write RGB triple to outfile
                for (int z = 0; z < n; z++) // Why can't I just set the number if fwrite = n?
                {
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr); // reading cursor probably left off right after BITMAPINFOHEADER in outfile.
                }
            }

            // add new padding to outfile
            for (int t = 0; t < new_padding; t++)
            {
                fputc(0x00, outptr);
            }
            //Send Cursor back/for loop?
            fseek(inptr, (-bi.biWidth*sizeof(RGBTRIPLE)), SEEK_CUR);
        }

        // iterate over pixels in scanline
        for (int a = 0; a < bi.biWidth; a++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr); // reading cursor probably left off right after BITMAPINFOHEADER in infile.

            // write RGB triple to outfile
            for (int b = 0; b < n; b++) // Why can't I just set the number if fwrite = n?
            {
            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr); // reading cursor probably left off right after BITMAPINFOHEADER in outfile.
            }
        }

        // add new padding to outfile
        for (int k = 0; k < new_padding; k++)
        {
            fputc(0x00, outptr);
        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR); // fread skips over padding in scanline of infile.
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
