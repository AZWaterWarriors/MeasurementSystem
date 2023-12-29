all: measure

.PHONY: clean spotless rpigpio

rpigpio:
	cd rpigpio ; make

measure: main.c rpigpio
	cc -g -o measure main.c -L./rpigpio -lrpigpio

clean:

spotless:
	rm -rf *.a measure
