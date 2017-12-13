/********************************************************
 * Original version of the code produced to just		*
 * request several seconds worth of data, and saving    *
 * directly to the folder that the program is contained	*
 * in. This iteration works and does not need to 		*
 * be touched.											*
 ********************************************************/
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <termios.h>
#include <errno.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <time.h>
#include <features.h>
#include <errno.h>
#include "structdef.h"
#include "func.h"

#define PRINT_OPAQUE_STRUCT(p)  print_mem((p), sizeof(*(p)))

typedef unsigned long dword;
typedef unsigned short word;
typedef unsigned int uniint32;
typedef unsigned char byte;

int main()
{
	byte commandflag = 0x7E; //flag used to let Datex know a command is being sent
	byte checksum; //sum of the total bytes sent
	
	FILE * f = fopen("Packet.txt", "w");
	
	int fd0;
	fd0 = open( "/dev/ttyUSB0", O_RDWR | O_NOCTTY | O_NDELAY );
	printf("%d \n", fd0);
	if(fd0 < 0)
	{
		printf("No valid connection \n");
		return 0;
	} 
	
	struct termios options; //creates struct to allow for changing of parameters
	
	tcgetattr(fd0, &options); //gets the attributes of the device
	cfsetispeed(&options, B19200); //sets in baud rate to 19200
	cfsetospeed(&options, B19200); //sets out baud rate to 19200
	
	options.c_cflag |= (CLOCAL | CREAD); //allows for write and read
	options.c_cflag |= PARENB;
	options.c_cflag &= ~PARODD;
	options.c_cflag &= ~CSTOPB;
	options.c_cflag &= ~CSIZE;
	options.c_cflag |= CS8;
	
	options.c_cflag |= CRTSCTS; //enables hardware flow

	options.c_lflag &= ~(ICANON | ECHO | ISIG); //raw input
	
	//options.c_iflag |= (IXON | IXOFF | IXANY); //software flow control

	options.c_cc[VTIME] = 0; // timer
	options.c_cc[VMIN] = 2; // blocks read until 2 chars received

	tcsetattr(fd0, TCSANOW, &options); //makes changes corresponding to the above parameters
	
	struct datex_hdr headerreq;
	struct datex_record requestPkt;
	struct wf_req *pRequest;

	//Clear the packet
	memset (&requestPkt, 0x00, sizeof(datex_record));
	
	//Fill the header
	requestPkt.hdr.r_len = sizeof(datex_hdr) + sizeof(struct wf_req); //length
	printf("%d \n", requestPkt.hdr.r_len);
	printf("%x \n", requestPkt.hdr.r_len);
	//requestPkt.hdr.r_nbr = 1; //record number
	requestPkt.hdr.r_maintype = 1; //main type of the record
	//requestPkt.hdr.dri_level = 0x3; //interface level
	//requestPkt.hdr.plug_id = 1; //ECG plug?
	//requestPkt.hdr.r_time = 0; //Epoch time
	
	
	
	//The packet contains only one subrecord
	// 0  = Waveform data transmission request
	requestPkt.hdr.sr_desc[0].sr_type = 0;
	requestPkt.hdr.sr_desc[0].sr_offset = 0;
	requestPkt.hdr.sr_desc[1].sr_type = 0xFF;
	
	//Fill the request
	pRequest = (wf_req *)&(requestPkt.rcrd.wf_rcrd);
	pRequest->req_type = 0;
	
	//Only one waveform type is requested
	pRequest->type[0] = 1;
	pRequest->type[1] = 0xFF;
	
	//print_mem((void*)&requestPkt, requestPkt.hdr.r_len);
	
	int ret[1250];
	int checkr;
	int checkw;

	unsigned char const *structarray = (void *)&requestPkt;
	checksum = structarray[0];
	for(int i = 0; i < checksum; i++)
	{
		printf("%02x ", structarray[i]);
		if(i%20 == 0 && i!=0)
			printf("\n");
	}
	printf("\n");
	write(fd0, (void *)&commandflag, 1);

	printf("\n");
	checkw = write(fd0, (void *)&requestPkt, checksum);
	write(fd0, (void *)&checksum, 1);
	write(fd0, (void *)&commandflag, 1);
	int finishchar[2];
	int j = 1;
	int headercount = 0;
	int line = 0;
	int flipflag = 0;
	int flipbuff = 0;
	int timebuff1 = 0;
	int timebuff2 = 0;
	int timebuff3 = 0;
	int timebuff4 = 0;
	int loopcount = 0;
	int packetcount = 0;
	int counter = 0;
	int buffflag = 0;
	int buffer = 0;
	int calcbuff = 0;
	int firstnumber = 0;
	int secondnumber = 0;
	int initnumb = 0;
	int MSB = 0;
	int LSB = 0;
	int nMSB = 0;
	int nLSB = 0;
	int preval = 0;
	int curval = 0;
	int difval = 0;
	int skipflag = 0;
	int looper;
	puts("Input the amount of seconds required to collect");
	scanf("%d", &looper);
	while(loopcount < looper)
	{
		while(headercount < 47)
		{
			usleep(5000);
			checkr = read(fd0, finishchar,1);
			if(checkr > 0)
			{
				headercount += 1;
				if(headercount == 8)
					timebuff1 = finishchar[0];
				else if(headercount == 9)
					timebuff2 = finishchar[0];
				else if(headercount == 10)
					timebuff3 = finishchar[0];
				else if(headercount == 11)
				{
					timebuff4 = finishchar[0];
					printf("%02x ", finishchar[0]);
					line += 1;
					if(line % 10 == 0)
					{
						printf("\n");
					}
					printf("%02x ", timebuff3);
					line += 1;
					if(line % 10 == 0)
					{
						printf("\n");
					}
					printf("%02x ", timebuff2);
					line += 1;
					if(line % 10 == 0)
					{
						printf("\n");
					}
					printf("%02x ", timebuff1);
					line += 1;
					if(line % 10 == 0)
					{
						printf("\n");
					}
				}	
				else if(finishchar[0] == 0x7E)
				{
					printf("%02x ", finishchar[0]);
					line += 1;
					if(line % 10 == 0)
					{
						printf("\n");
					}
				}
				else
				{
					if(flipflag == 0)
					{
						flipbuff = finishchar[0];
						flipflag = 1;
					}
					else
					{
						printf("%02x ", finishchar[0]);
						line += 1;
						if(line % 10 == 0)
						{
							printf("\n");
						}
						printf("%02x ", flipbuff);
						line += 1;
						if(line % 10 == 0)
						{
							printf("\n");
						}
						flipflag = 0;
					}
				}
			}
		}
		printf("\nHEADER COMPLETE \n");
		time_t totaltime = 0;
		printf("Timebuff1: %d\n Timebuff2:%d\n Timebuff3:%d\n Timebuff4:%d \n", timebuff1, timebuff2, timebuff3, timebuff4);
		totaltime = timebuff1 + timebuff2 * 256 + timebuff3 * 65536 + timebuff4 * 16777216 - 36000;
		unixtime(totaltime);
		line = 0;
		packetcount = 0;
		buffflag = 0;
		buffer = 0;
		calcbuff = 0;
		firstnumber = 1;
		secondnumber = 0;
		initnumb = 1;
		preval = 0;
		curval = 0;
		while(packetcount < 1)
		{
			usleep(125);
			checkr = read(fd0,finishchar,1);
			if(initnumb == 1)
			{
				if(finishchar[0] == 0x00 || finishchar[0] == 0xFF)
				{
					checkr = read(fd0, finishchar, 1);
				}
				initnumb = 0;
			}
			printf("%02x ", finishchar[0]);
			line += 1;
			if(line % 10 == 0)
			{
				printf("\n");
			}
			if(finishchar[0] == 0x7E)
				packetcount += 1;
			else if(firstnumber == 1)
			{
				firstnumber = 0;
				secondnumber = 1;
				LSB = finishchar[0];
				if(finishchar[0] == 0x7D)
				{
					read(fd0,finishchar,1);
					if(finishchar[0] == 0x5E)
						LSB = 0x7E;
					else if(finishchar[0] == 0x5D)
						LSB = 0x7D;
					else
						LSB = finishchar[0];
				}		
			}
			else if(secondnumber == 1)
			{
				firstnumber = 1;
				secondnumber = 0;
				MSB = finishchar[0];
				if(finishchar[0] > 0xF0)
				{
					nMSB = MSB - 0xFF;
					nLSB = LSB - 0xFF - 0x01;
					curval = nMSB * 256 + nLSB;
				}
				else
				{
					curval = MSB * 256 + LSB;
				}
				if(preval == 0)
					preval = curval;
				else
				{
					difval = abs(preval - curval);
					if(difval > 512)
					{
						LSB = MSB;
						skipflag = 1;
					}
					else
						preval = curval;
				}
				if(skipflag == 1)
				{
					skipflag = 0;
					secondnumber = 1;
					firstnumber = 0;
				}
				else
				{
					counter += 1;
					fprintf(f, "%d %d \n", counter, curval);
				}
			}
			
		}
	
	packetcount = 0;
	headercount = 0;
	loopcount += 1;
	line = 0;
	printf("\n");
	}
	printf("NUMBER OF DATA = %d \n", counter);
	fclose(f);
	system("gnuplot -p -e \"plot 'Packet.txt' with linespoints ls 1\"");
	getchar();
	
	// Request stopping data
	memset(&requestPkt, 0x00, sizeof(datex_record));
	
	requestPkt.hdr.r_len = sizeof(datex_hdr) + sizeof(struct wf_req);
	requestPkt.hdr.r_maintype = 1;
	
	requestPkt.hdr.sr_desc[0].sr_type = 0;
	requestPkt.hdr.sr_desc[0].sr_offset = (byte)0;
	requestPkt.hdr.sr_desc[1].sr_type = (short)0xFF;
	
	pRequest = (wf_req *)&(requestPkt.rcrd.wf_rcrd);
	pRequest->req_type = 1;
	pRequest->type[0] = 0xFF;
	
	structarray = (void *)&requestPkt;
	checksum = structarray[0];
	write(fd0, (void *)&commandflag, 1);

	checkw = write(fd0, (void *)&requestPkt, checksum);
	write(fd0, (void *)&checksum, 1);
	write(fd0, (void *)&commandflag, 1);
	return 0;
}
