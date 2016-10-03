#ifndef PART1_H
#define PART1_H

// defining board struct
typedef struct {
    int *array;
    int size;
    int numQueens;
} Board_t;

// defining lookup table collection struct
typedef struct {
    int *hlist; // Horizontal list
    int *d1list; // Down right list
    int *d2list; // Down left list
    int **hlup; // Lookup table for horizontal list
    int **d1lup; // Lookup for down right list
    int **d2lup; // Lookup for down left list
} Lookup_t;

// declaring functions
int toInt(char *s);
int *toIntArray(char *s, int size);
char *getInput(char *message);
Board_t *copy_Board_t(Board_t *orig);
void freeBoard(Board_t *board);
void printBoard_t(Board_t *board, int ending);
void initLookupTable(Lookup_t *lup, int n);
void generateLup(Lookup_t *lup, int n);
void addPos(Lookup_t *lup, int col, int row);
void remPos(Lookup_t *lup, int col, int row);
int checkPos(Lookup_t *lup, int col, int row);
void backtrack(Board_t *board, Lookup_t *lup, int *nsols, long myID);
void *runThread(void *tid);


#endif
