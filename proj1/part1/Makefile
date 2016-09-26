CC=gcc
CFLAGS=-I. -Wall
DEPS = part1.h
OBJ = part1.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

part1: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)

.PHONY: clean
clean:
	rm -f $(OBJ) part1
