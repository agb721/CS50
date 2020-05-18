// INCOMPLETE. My first recursive function :-) Written to solidify my thinking about the following riddle (essentially the "n of k" problem in statistics):
// You have a party where each guest toasts exactly once with each other guest.
// A total of 55 toasts are made at the party. How many guests were present?
// Ideally: prints the total number of unique groupings of size (n) you can get from a group of (k) people.

#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Decrale funciton prototype
int nofk (int a, int b);

int main()
{
    // # size of each grouping / combination
    int n = 3;
    // total party size / people present
    int k = 11;
    // Print the total number of possible groupings
    printf("%i\n", nofk(n,k));
}

// Define recursive permutation function
int nofk (int n, int k)
{
    // Quit if variables are invalid
    if (n > k || k < 2)
    {
        printf( "Invalid value pairing.");
        return 0;
    }
    // Base condition
    if (k == 2)
    {
        return 1;
    }
    return (k-1) + (nofk(n,(k-1)));
}