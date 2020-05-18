#include <stdio.h>
#include <stdlib.h>
// recovers deleted image files


int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }

    // open input file
    FILE *fileptr = fopen(argv[1], "r");
    if (fileptr == NULL)
    {
        fprintf(stderr, "Could not open file\n");
        return 2;
    }

    // initiate counter for JPEG names
    int counter = 0;
    // create buffer
    unsigned char buffer[512];
    // create pointer for writing file
    FILE *img = NULL;
    // create indicator variable to that changes value when eof is reached
    int eof_indicator = 0;

    // iterate until end of card
    do
    {
        // read 512 bytes into buffer and check for eof
        if (fread(&buffer, 1, 512, fileptr) != 512) //code only worked if this was one line, probably bc using fread to only check a condition moved things too much
        {
            eof_indicator = 1;
            fclose(img); // putting this here was crucial
        }
        // identify beginning of a JPEG
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (counter == 0) // notice that what happens in this subsectin is a bit redundant -- try to condense the code that repeats itself
            {
                // Create new JPEG
                char filename[8];
                sprintf(filename, "%03i.jpg", counter);
                img = fopen(filename, "w"); //not sure what exactly happens here

                // Write buffer to new file
                fwrite(&buffer, 512, 1, img);
                counter++;
            }
            else
            {
                //close previous imgage
                fclose(img);

                // Create new JPEG
                char filename[8];
                sprintf(filename, "%03i.jpg", counter);
                img = fopen(filename, "w"); //not sure what exactly happens here

                // Write buffer to new file
                fwrite(&buffer, 512, 1, img);
                counter++;
            }
        }
        else
        {
            if (counter == 0)
            {
                //do nothing
            }
            else
            {
                // keep writing
                fwrite(&buffer, 512, 1, img);
            }
        }
    }
    while (eof_indicator != 1);

    fclose(fileptr);
}
