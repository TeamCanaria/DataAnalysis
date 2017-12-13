CC=gcc `pkg-config --cflags --libs gtk+-2.0` -std=gnu99

main.o: main.c func.h datacollectionfunc.h structdef.h
	$(CC) -c main.c
DatexConnectionSoftware: main.o
	$(CC) -o DatexConnectionSoftware main.o
