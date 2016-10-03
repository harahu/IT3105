/*
Solution to n-queen problem by using backtracking

INPUT:
    n integers
        ex: 1 2 3 4 0 0 0 0
    input refers to the row for a queen in each column
    0 means empty column

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <pthread.h>

#include "part2.h"


#define MAX_INPUT_SIZE 128
#define STEPS 0  // 1 - pauses every step, 0 - no pause

/* Threading specific global variables */
int numThreads;
pthread_t *threads;
pthread_mutex_t nsolsmutex;

/* Global variables used */
Board_t *startboard;
int *sumnsols;
int *chunks; // Array containing the work chunk portions 

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

/* Allocate arrays to be used in Lookup_t */
void initLookupTable(Lookup_t *lup, int n) {
    lup->hlist = (int*)calloc(n, sizeof(int));
    lup->hlup = (int**)malloc(sizeof(int*)*n*n);
    lup->d1list = (int*)calloc((n*2-1), sizeof(int));
    lup->d1lup = (int**)malloc(sizeof(int*)*n*n);
    lup->d2list = (int*)calloc((n*2-1), sizeof(int));
    lup->d2lup = (int**)malloc(sizeof(int*)*n*n);
}

/* Generate lookup table */
void generateLup(Lookup_t *lup, int n) {
    // Initialize horizontal list
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            lup->hlup[i*n + j] = &(lup->hlist[i]);
        }
    }
    
    // Initialize first diagonal list
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            lup->d1lup[i*n + j] = &(lup->d1list[i+j]);
        }
    }
    
    // Initialize second diagonal list
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            lup->d2lup[i*n + j] = &(lup->d2list[(n-i-1)+j]);
        }
    }
}

/* Add position to lookup table */
void addPos(Lookup_t *lup, int col, int row){
    int n = startboard->size;
    *(lup->hlup)[row*n + col] = 1;
    *(lup->d1lup)[row*n + col] = 1;
    *(lup->d2lup)[row*n + col] = 1;
}

/* Remove position from lookup table */
void remPos(Lookup_t *lup, int col, int row){
    int n = startboard->size;
    *(lup->hlup)[row*n + col] = 0;
    *(lup->d1lup)[row*n + col] = 0;
    *(lup->d2lup)[row*n + col] = 0;
}

/* Check position in lookup table */
int checkPos(Lookup_t *lup, int col, int row){
    int n = startboard->size;
    return (1-*(lup->hlup)[row*n + col]) * (1-*(lup->d1lup)[row*n + col]) * (1-*(lup->d2lup)[row*n + col]);
}

/* Backtracking recursive function */
void backtrack(Board_t *board, Lookup_t *lup, int *nsols, long myID) {
    Board_t *curboard = copy_Board_t(board);
    int size = curboard->size;
    int pos = curboard->numQueens;
    int startRow;
    int stopRow;
    
    if (STEPS) {
        printBoard_t(curboard, 0);
        printf(" Starting on column %i", pos+1);
        getchar();
    }
    
    if (pos != startboard->numQueens) {
        startRow = 1;
        stopRow = size+1;
    } else {
        startRow = chunks[myID];
        stopRow = chunks[myID+1];
    }
    
    curboard->numQueens++;
    for (int i = startRow; i < stopRow; i++) { // loop rows
        curboard->array[pos] = i;
        if (checkPos(lup, pos, i-1) == 1) {
            // current board is fine
            
            if (STEPS) {
                printBoard_t(curboard, 0);
                printf(" Column %i, queen at row %i is fine", pos+1, i);
                getchar();
            }
            
            addPos(lup, pos, i-1);
            if (curboard->array[size-1] != 0) {
                // solution to n-queen
                (*nsols)++;
                /*
                if (STEPS) {
                    printBoard_t(curboard, 0);
                    printf(" This board is a soluton");
                    getchar();
                } else {
                    printBoard_t(curboard, 0);
                    printf(" is a solution\n");
                }*/
            } else {
                backtrack(curboard, lup, nsols, myID); // go further in
                // no (more) solutions further in using curboard
                if (STEPS) {
                    printBoard_t(curboard, 0);
                    printf(" Found no more solutions at column %i, going back", pos+2);
                    getchar();
                }
            }
            remPos(lup, pos, i-1);
        }
    }
    freeBoard(curboard);
    // no (more) solutions further in using board
}

/* Every thread will run this function */
void *runThread(void *tid) {
    long myID = (long) tid;
    int *nsols = malloc(sizeof(int));
    
    Lookup_t *lup = malloc(sizeof(Lookup_t));
    
    // Generate the lookup table
    initLookupTable(lup, startboard->size);
    generateLup(lup, startboard->size);
    
    // Add initial board to lookup table
    for (int pos = 0; pos < startboard->numQueens; pos++) {
        if (checkPos(lup, pos, startboard->array[pos]-1) == 0) {
            printf("Found 0 solutions\n");
            exit(0);
        }
        addPos(lup, pos, startboard->array[pos]-1);
    }
    
    backtrack(startboard, lup, nsols, myID);
    
    pthread_mutex_lock(&nsolsmutex);
    (*sumnsols) += (*nsols);
    pthread_mutex_unlock(&nsolsmutex);
}


int main(int argc, char** argv) {
    startboard = (Board_t*)malloc(sizeof(Board_t));
    sumnsols = (int*)malloc(sizeof(int)); // number of solutions
    int n;
    int *qdata; // queen data (temporary list)
    
    // Get initial board
    if (argc == 1) {
        char *threadsRaw = getInput("Specify the number of threads: ");
        numThreads = toInt(threadsRaw);
        free(threadsRaw);
        
        char *nsizeRaw = getInput("Specify the n in n-queens: ");
        n = toInt(nsizeRaw);
        free(nsizeRaw);
        
        char *dataRaw = getInput("Enter queen positions: ");
        qdata = toIntArray(dataRaw, n);
        free(dataRaw);
    } else {
        n = argc-2;
        qdata = (int*)malloc(sizeof(int)*n);
        
        numThreads = toInt(argv[1]);
        
        for (int i = 0; i < n; i++) {
            qdata[i] = toInt(argv[i+2]);
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
    
    chunks = malloc(sizeof(int) * (numThreads+1));
    chunks[0] = 1;
    chunks[numThreads] = n+1;
    for (int i = 1; i < numThreads; i++) {
        chunks[i] = (int) i*n/numThreads;
    }
    
    *sumnsols = 0; // initialize number of solutions
    
    threads = (pthread_t*)malloc(sizeof(pthread_t) * numThreads);
    
    /* Generate threads and run runThread() */
    for (long i = 0; i < numThreads; i++) {
        pthread_create(&threads[i], NULL, runThread, (void*) i);
    }
    
    /* Wait for threads to finish */
    for (long i = 0; i < numThreads; i++) {
        pthread_join(threads[i], NULL);
    }
    
    printf("Found %i solutions\n", *sumnsols);
}
