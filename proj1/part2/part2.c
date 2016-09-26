/*
Solution to 8-queen problem by using backtracking

INPUT:
    8 integers
        ex: 1 2 3 4 0 0 0 0
    input refers to the row for a queen in each column
    0 means empty


Hans-Kristian Bruvold
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "part2.h"


#define MAX_INPUT_SIZE 128
#define STEPS 0  // 1 - pauses every step, 0 - no pause

/* Convert a string to integer
 * Expects a single integer without any spaces
 */
int toInt(char *s) {
    int value = strtol(s, NULL, 10);
    
    return value;
}

/* Convert a string to an array of integers
 * Expects integers to be separated by space
 */
int *toIntArray(char *s, int size) {
    int *values = (int*) malloc(size * sizeof(int));
    char **endptr = &s;
    
    for (int i = 0; i < size; i++) {
        values[i] = strtol(*endptr, endptr, 10);
    }
    
    return values;
}

/* Get input from user */
char *getInput(char *message) {
    char *rawInput = (char*)malloc(MAX_INPUT_SIZE);
    if (rawInput == NULL) {
        printf("Unable to allocate memory for input data\n");
        return NULL;
    }
    
    printf("%s", message);
    fgets(rawInput, MAX_INPUT_SIZE, stdin);
    
    // remove trailing newline
    if ((strlen(rawInput) > 0) && (rawInput[strlen(rawInput)-1] == '\n')) {
        rawInput[strlen(rawInput)-1] = '\0';
    }
    
    return rawInput;
}

/* Copy a Board_t struct */
Board_t *copy_Board_t(Board_t *orig) {
    Board_t *temp = (Board_t*)malloc(sizeof(Board_t));
    int *array = (int*)malloc(sizeof(int) * orig->size);
    
    memcpy(temp, orig, sizeof(Board_t));
    memcpy(array, orig->array, sizeof(int) * orig->size);
    temp->array = array;
    return temp;
}

/* Delete a Board_t struct */
void freeBoard(Board_t *board) {
    free(board->array);
    free(board);
}

/* Print Board_t data
 * ending = 1: print ending with '\n'
 */
void printBoard_t(Board_t *board, int ending) {
    printf("[%i", board->array[0]);
    for (int i = 1; i < board->size; i++) {
        printf(" %i", board->array[i]);
    }
    printf("]");
    if (ending)
        printf("\n");
}

/* Generate lookup table */
void generateLup(int *hlist, int **hlup, int *d1list, int **d1lup, int *d2list, int **d2lup, int n) {
    // Initialize horizontal list
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            hlup[i*n + j] = &hlist[i];
        }
    }
    
    // Initialize first diagonal list
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            d1lup[i*n + j] = &d1list[i+j];
        }
    }
    
    // Initialize second diagonal list
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            d2lup[i*n + j] = &d2list[(n-i-1)+j];
        }
    }
}

/* Add position to lookup table */
void addPos(int **hlup, int **d1lup, int **d2lup, int n, int col, int row){
    *hlup[row*n + col] = 1;
    *d1lup[row*n + col] = 1;
    *d2lup[row*n + col] = 1;
}

/* Remove position from lookup table */
void remPos(int **hlup, int **d1lup, int **d2lup, int n, int col, int row){
    *hlup[row*n + col] = 0;
    *d1lup[row*n + col] = 0;
    *d2lup[row*n + col] = 0;
}

/* Check position in lookup table */
int checkPos(int **hlup, int **d1lup, int **d2lup, int n, int col, int row){
    return (1-*hlup[row*n + col]) * (1-*d1lup[row*n + col]) * (1-*d2lup[row*n + col]);
}

/* Backtracking recursive function */
void backtrack(Board_t *board, int **hlup, int **d1lup, int **d2lup, int *nsols) {
    Board_t *curboard = copy_Board_t(board);
    int size = curboard->size;
    int pos = curboard->numQueens;
    
    if (STEPS) {
        printBoard_t(curboard, 0);
        printf(" Starting on column %i", pos+1);
        getchar();
    }
    
    curboard->numQueens++;
    for (int i = 1; i < size+1; i++) { // loop rows
        curboard->array[pos] = i;
        if (checkPos(hlup, d1lup, d2lup, curboard->size, pos, i-1) == 1) {
            // current board is fine
            
            if (STEPS) {
                printBoard_t(curboard, 0);
                printf(" Column %i, queen at row %i is fine", pos+1, i);
                getchar();
            }
            
            addPos(hlup, d1lup, d2lup, curboard->size, pos, i-1);
            if (curboard->array[size-1] != 0) {
                // solution to n-queen
                (*nsols)++;
                if (STEPS) {
                    printBoard_t(curboard, 0);
                    printf(" This board is a soluton");
                    getchar();
                } else {
                    printBoard_t(curboard, 0);
                    printf(" is a solution\n");
                }
            } else {
                backtrack(curboard, hlup, d1lup, d2lup, nsols); // go further in
                // no (more) solutions further in using curboard
                if (STEPS) {
                    printBoard_t(curboard, 0);
                    printf(" Found no more solutions at column %i, going back", pos+2);
                    getchar();
                }
            }
            remPos(hlup, d1lup, d2lup, curboard->size, pos, i-1);
        }
    }
    freeBoard(curboard);
    // no (more) solutions further in using board
}


int main(int argc, char** argv) {
    Board_t *startboard = (Board_t*)malloc(sizeof(Board_t));
    int *nsols = (int*)malloc(sizeof(int)); // number of solutions
    int n;
    int *qdata; // queen data (temporary list)
    
    // Declare some variables to be used in lookup method
    int *hlist; // Horizontal list
    int **hlup; // Lookup table for horizontal list
    int *d1list; // Down right list
    int **d1lup;
    int *d2list; // Down left list
    int **d2lup;
    
    // Get initial board
    if (argc == 1) {
        char *nsizeRaw = getInput("Specify the n in n-queens: ");
        n = toInt(nsizeRaw);
        free(nsizeRaw);
        
        char *dataRaw = getInput("Enter queen positions: ");
        qdata = toIntArray(dataRaw, n);
        free(dataRaw);
    } else {
        n = argc-1;
        qdata = (int*)malloc(sizeof(int)*n);
        
        for (int i = 0; i < n; i++) {
            qdata[i] = (int) (*argv[i+1] - '0');
        }
    }
    
    // Add data to startboard struct
    startboard->size = n;
    startboard->array = qdata;
    startboard->numQueens = n;
    
    // Update number of set queens to struct
    for (int i = 0; i < n; i++) {
        if (qdata[i] == 0) {
            startboard->numQueens = i;
            break;
        }
    }
    
    // Generate the lookup table
    hlist = (int*)calloc(n, sizeof(int));
    hlup = (int**)malloc(sizeof(int*)*n*n);
    d1list = (int*)calloc((n*2-1), sizeof(int));
    d1lup = (int**)malloc(sizeof(int*)*n*n);
    d2list = (int*)calloc((n*2-1), sizeof(int));
    d2lup = (int**)malloc(sizeof(int*)*n*n);
    generateLup(hlist, hlup, d1list, d1lup, d2list, d2lup, n);
    
    // Add initial board to lookup table
    for (int pos = 0; pos < startboard->numQueens; pos++) {
        addPos(hlup, d1lup, d2lup, n, pos, qdata[pos]-1);
    }
    
    *nsols = 0; // initialize number of solutions
    
    /* Ready to run backtrack algorithm */
    backtrack(startboard, hlup, d1lup, d2lup, nsols);
    printf("Found %i solutions\n", *nsols);
}
