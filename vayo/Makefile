CFLAGS= -O2 -Wall
OBJS= sony-fnkey.o utility.o osd.o

all: $(OBJS)
	gcc $(CFLAGS) $(OBJS) -o sony-fnkey -lxosd

install: sony-fnkey
	install --mode=755 sony-fnkey /usr/local/bin

clean:
	rm -f sony-fnkey *.o


.PHONY: install clean
