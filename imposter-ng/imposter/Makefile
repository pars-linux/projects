
CC= gcc
CFLAGS= -O2 -Wall -Iinclude -DHAVE_CONFIG_H=1

OBJS = \
	src/document.o \
	src/render.o \
	src/r_back.o \
	src/r_style.o \
	src/r_geometry.o \
	src/r_gradient.o \
	src/r_draw.o \
	src/zip.o \
	src/iksemel.o

libimposter.a: $(OBJS)
	ar r $@ $(OBJS)

clean:
	rm -f libimposter.a src/*.o
