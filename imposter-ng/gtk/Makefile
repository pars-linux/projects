
GTK_CFLAGS = `pkg-config --cflags gtk+-2.0`
GTK_LIBS = `pkg-config --libs gtk+-2.0`
CC= gcc
CFLAGS= -O2 -Wall -DHAVE_CONFIG_H=1 -Iinclude -I../imposter/include $(GTK_CFLAGS)

OBJS = \
	src/main.o \
	src/render.o \
	src/ui.o \
	src/debug.o \
	src/slave.o \
	src/gtkutility.o \
	src/about.o

imposter: $(OBJS) ../imposter/libimposter.a
	$(CC) -o $@ $(OBJS) $(GTK_LIBS) -L../imposter -limposter

clean:
	rm -f imposter src/*.o
