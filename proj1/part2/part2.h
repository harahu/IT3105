#ifndef PART1_H
#define PART1_H

// defining board struct
typedef struct {
    int *array;
    int size;
    int numQueens;
} Board_t;

// declaring functions
int toInt(char *s);
int *toIntArray(char *s, int size);
char *getInput(char *message);
Board_t *copy_Board_t(Board_t *orig);
void freeBoard(Board_t *board);
void printBoard_t(Board_t *board, int ending);
void generateLup(int *hlist, int **hlup, int *d1list, int **d1lup, int *d2list, int **d2lup, int n);
void addPos(int **hlup, int **d1lup, int **d2lup, int n, int col, int row);
void remPos(int **hlup, int **d1lup, int **d2lup, int n, int col, int row);
int checkPos(int **hlup, int **d1lup, int **d2lup, int n, int col, int row);
void backtrack(Board_t *board, int **hlup, int **d1lup, int **d2lup, int *nsols);


#endif
