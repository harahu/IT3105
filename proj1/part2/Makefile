CC=gcc
CFLAGS=-I. -O3 -Wall
DEPS = part2.h
OBJ = part2.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

part2: $(OBJ)
	gcc -o $@ $^ $(CFLAGS)

.PHONY: clean
clean:
	rm -f $(OBJ) part2
