
CC = gcc
CFLAGS = -g -Wall

LIBS := -lX11 -lXtst
SOURCES = f5.c

TARGET = f5


all: $(TARGET)

$(TARGET):
	$(CC) $(CFLAGS) $(SOURCES) $(LIBS) -o $(TARGET)

clean:
	rm -f $(TARGET)

