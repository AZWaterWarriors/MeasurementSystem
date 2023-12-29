all: measure

.PHONY: clean spotless

measure: main.c
	cc -o measure main.c

clean:

spotless:
	rm -rf *.a measure
