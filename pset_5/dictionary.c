// Implements a dictionary's functionality by organizing dicitonary words in side a hash table.
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1000;
// Counter for words loaded into dictionary
int counter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Create cursor
    node *cursor = table[hash(word)];
    // Run cursor through linked list at words
    while (cursor != NULL) // Note to self: before I had: (cursor->next != NULL) -- bug solved and understood.
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number between 0 and N
// Funciton taken from https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9189q/ posted by delipity
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    for (int j = 0, n = strlen(word); j < n; j++)
    {
        hash = (hash << 2) ^ tolower(word[j]);
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Can't open dictionary.\n");
        return false;
    }

    // Variables
    char word[LENGTH + 1];
    int value = 0;

    // Read strings from dictionary file, one at a time
    while (fscanf(file, "%s", word) != EOF)
    {
        // Read from file into word buffer
        // Create new node
        node *n = malloc(sizeof(node));
        strcpy(n->word, word);
        n->next = NULL;
        // Hash word to obtain hash value
        value = hash(word);
        // Insert node into hash table at starting location
        n->next = table[value];
        table[value] = n;
        counter++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded
unsigned int size(void)
{
    return  counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *cursor = NULL;
    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}

