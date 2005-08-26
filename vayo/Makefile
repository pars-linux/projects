CFLAGS= -O2 -Wall
OBJS= sony-fnkey.o utility.o osd.o

all: $(OBJS)
	gcc $(CFLAGS) $(OBJS) -o sony-fnkey -lxosd

clean:
	rm -f sony-fnkey *.o
