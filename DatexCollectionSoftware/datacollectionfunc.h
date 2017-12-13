/****************************************************
 * This header contains a variety of functions		*
 * that are used to collect data from the Datex and	*
 * send them to a file. 							*
 ****************************************************/
typedef unsigned long dword;
typedef unsigned short word;
typedef unsigned int uniint32;
typedef unsigned char byte;

#include <gtk/gtk.h>
#include <sys/stat.h>
#include <sys/mount.h>

/************************************************
 * This function runs before data is collected  *
 * from the Ohmeda Datex. It continually polls  *
 * the machine for the time in the header and   *
 * compares it to the time given via the GUI.   *
 * If they match, the function ends.            *
 ************************************************/
void begindatacollection(time_t starttime, int fd0)
{
	int timeflag = 0; //flag to indicate if packettime is greater than start time
	int finishchar[2];//variable where data from the Datex is stored
	int headercount = 0; //counter used to store the number of characters read in the header
	int line = 0; //variable used for debugging purposes to create new lines
	int flipflag = 0; //flag to indicate when two incoming data values need to be flipped
	int flipbuff = 0; //variable used to store the value that needs to be flipped
	int timebuff1 = 0; //stores the least significant bit of the time value 
	int timebuff2 = 0; //stores the second least significant bit of the time value 
	int timebuff3 = 0; //stores the second most significant bit of the time value 
	int timebuff4 = 0; //stores the most significant bit of the time value 
	int loopcount = 0; //variable to count the loop of a second
	int packetcount = 0; //variable to count the amount of values in a second
	int firstnumber = 0; //flag used to indicate if the value is the first of two numbers that make up a value
	int secondnumber = 0; //flag used to indicate if the value is the second of two numbers that make up a value
	int initnumb = 0; //flag used to indicate if the value is the first of number of the packet
	int MSB = 0; //variable used to store the most significant bit of a value
	int LSB = 0; //variable used to store the least significant bit of a value
	int nMSB = 0; //variable used to store the most significant bit of a value if negative
	int nLSB = 0; //variable used to store the least significant bit of a value if negative
	int preval = 0; //variable used to store the previous value
	int curval = 0; //variable used to store the current value
	int difval = 0; //variable used to store the difference between the previous and current values
	int skipflag = 0; //flag used to skip a value if the difference is too great
	int checkr = 0; //variable used to check if a bit has been read from the Datex
	while(timeflag == 0) //loop until the packet time is greater than the starting time
	{
		while(headercount < 47) //loop until all 47 characters of the header are read
		{
			usleep(1667);
			checkr = read(fd0, finishchar,1); //read in the character
			if(checkr > 0)
			{
				headercount += 1; //increment header count
				if(headercount == 8) //indicates part of the time variable
					timebuff1 = finishchar[0];
				else if(headercount == 9) //indicates part of the time variable
					timebuff2 = finishchar[0];
				else if(headercount == 10) //indicates part of the time variable
					timebuff3 = finishchar[0];
				else if(headercount == 11) //indicates part of the time variable
					timebuff4 = finishchar[0];
				if(finishchar[0] == 0x7D) //0x7E is a command variable, so 0x7D + 0x5E = 0x7E, and 0x7D + 0x5D = 0x7D
				{
					read(fd0,finishchar,1);
					if(finishchar[0] == 0x5E)
						finishchar[0] = 0x7E;
					else if(finishchar[0] == 0x5D)
						finishchar[0] = 0x7D;
				}		
			}
		}
		time_t totaltime = 0;
		totaltime = timebuff1 + timebuff2 * 256 + timebuff3 * 65536 + timebuff4 * 16777216 - 36000; //calculates time total from given packet
		printf("\n");
		//prints unix time of both for debugging purposes
		unixtime(totaltime); 
		unixtime(starttime);
		if(totaltime >= starttime) //checks if the packet time is greater than the starting time given
			timeflag = 1;
		//resetting variables
		line = 0;
		packetcount = 0;
		firstnumber = 1;
		secondnumber = 0;
		initnumb = 1;
		preval = 0;
		curval = 0;
		while(packetcount < 1) //loops until 0x7E is read, indicating end of packet
		{
			usleep(125);
			checkr = read(fd0,finishchar,1);
			if(initnumb == 1) //checks the initial number given
			{
				if(finishchar[0] == 0x00 || finishchar[0] == 0xFF) //initial number cannot be these, removes it
				{
					checkr = read(fd0, finishchar, 1);
				}
				initnumb = 0;
			}
			if(finishchar[0] == 0x7E) //indicates that packet is complete
				packetcount += 1;
			else if(firstnumber == 1) //check for the first number of two for a value
			{
				firstnumber = 0; //drop flag of first value
				secondnumber = 1; //raise flag of second value
				LSB = finishchar[0]; //set LSB to most recently received value
				if(finishchar[0] == 0x7D) //0x7E is a command variable, so 0x7D + 0x5E = 0x7E, and 0x7D + 0x5D = 0x7D
				{
					read(fd0,finishchar,1); //read next value to determine true value
					if(finishchar[0] == 0x5E)
						LSB = 0x7E;
					else if(finishchar[0] == 0x5D)
						LSB = 0x7D;
					else
						LSB = finishchar[0];
				}		
			}
			else if(secondnumber == 1) //check for the second number of two for a valaue
			{
				firstnumber = 1; //drop flag of second value
				secondnumber = 0; //raise flag of first value
				MSB = finishchar[0]; //set MSB to most recently received value
				if(finishchar[0] > 0xF0) //check if the value is negative
				{
					//make changes to ensure negative number is displayed
					nMSB = MSB - 0xFF;
					nLSB = LSB - 0xFF - 0x01;
					curval = nMSB * 256 + nLSB; //store the most current value to curval
				}
				else
				{
					curval = MSB * 256 + LSB; //store the most current value to curval
				}
				if(preval == 0) //checks if the previous value is null
					preval = curval; //sets preval to the current value
				else
				{
					difval = abs(preval - curval); //stores the difference between the previous and current value
					if(difval > 512) //checks if the different value is too great
					{
						LSB = MSB;
						skipflag = 1;
					}
					else
						preval = curval; //sets the current value to preval
				}
				if(skipflag == 1) //checks if current bit needs to be skipped
				{
					skipflag = 0;
					secondnumber = 1;
					firstnumber = 0;
				}

			}
			
		}
	//reset packet and header count
	packetcount = 0; 
	headercount = 0;
	loopcount += 1; //indicates end of packet has been reached
	}
};
/******************************************************************************
 * This function is called once the time received from the datex is greater
 * than time given via the GUI. Creates multiple files in accordance with
 * the value of amount. */
void packetpull(time_t starttime, time_t endtime, int fd0, FILE *f)
{	
	int timeflag = 0; //flag to indicate if packettime is greater than start time
	int finishchar[2]; //variable where data from the Datex is stored
	int counter = 0; //counter used to count the amount of values in a file
	int headercount = 0; //counter used to store the number of characters read in the header
	int line = 0; //variable used for debugging purposes to create new lines
	int flipflag = 0; //flag to indicate when two incoming data values need to be flipped
	int flipbuff = 0; //variable used to store the value that needs to be flipped
	int timebuff1 = 0; //stores the least significant bit of the time value 
	int timebuff2 = 0; //stores the second least significant bit of the time value 
	int timebuff3 = 0; //stores the second most significant bit of the time value 
	int timebuff4 = 0; //stores the most significant bit of the time value 
	int loopcount = 0; //variable to count the loop of a second
	int packetcount = 0; //variable to count the amount of values in a second
	int firstnumber = 0; //flag used to indicate if the value is the first of two numbers that make up a value
	int secondnumber = 0; //flag used to indicate if the value is the second of two numbers that make up a value
	int initnumb = 0; //flag used to indicate if the value is the first of number of the packet
	int MSB = 0; //variable used to store the most significant bit of a value
	int LSB = 0; //variable used to store the least significant bit of a value
	int nMSB = 0; //variable used to store the most significant bit of a value if negative
	int nLSB = 0; //variable used to store the least significant bit of a value if negative
	int preval = 0; //variable used to store the previous value
	int curval = 0; //variable used to store the current value
	int difval = 0; //variable used to store the difference between the previous and current values
	int skipflag = 0; //flag used to skip a value if the difference is too great
	int checkr = 0; //variable used to check if a bit has been read from the Datex
	while(timeflag == 0)
	{
		while(headercount < 47)
		{
			usleep(1000);
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
				else //flip the two numbers, then print them to screen
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
		time_t totaltime = 0;
		totaltime = timebuff1 + timebuff2 * 256 + timebuff3 * 65536 + timebuff4 * 16777216 - 36000;
		printf("\n");
		unixtime(totaltime);
		unixtime(starttime);
		if(totaltime >= endtime)
			timeflag = 1;
		line = 0;
		packetcount = 0;
		firstnumber = 1;
		secondnumber = 0;
		initnumb = 1;
		preval = 0;
		curval = 0;
		while(packetcount < 1) //loops until 0x7E is read, indicating end of packet
		{
			usleep(125);
			checkr = read(fd0,finishchar,1);
			if(initnumb == 1) //checks the initial number given
			{
				if(finishchar[0] == 0x00 || finishchar[0] == 0xFF) //initial number cannot be these, removes it
				{
					checkr = read(fd0, finishchar, 1);
				}
				initnumb = 0;
			}
			if(finishchar[0] == 0x7E) //indicates that packet is complete
				packetcount += 1;
			else if(firstnumber == 1) //check for the first number of two for a value
			{
				firstnumber = 0; //drop flag of first value
				secondnumber = 1; //raise flag of second value
				LSB = finishchar[0]; //set LSB to most recently received value
				if(finishchar[0] == 0x7D) //0x7E is a command variable, so 0x7D + 0x5E = 0x7E, and 0x7D + 0x5D = 0x7D
				{
					read(fd0,finishchar,1); //read next value to determine true value
					if(finishchar[0] == 0x5E)
						LSB = 0x7E;
					else if(finishchar[0] == 0x5D)
						LSB = 0x7D;
					else
						LSB = finishchar[0];
				}		
			}
			else if(secondnumber == 1) //check for the second number of two for a valaue
			{
				firstnumber = 1; //drop flag of second value
				secondnumber = 0; //raise flag of first value
				MSB = finishchar[0]; //set MSB to most recently received value
				if(finishchar[0] > 0xF0) //check if the value is negative
				{
					//make changes to ensure negative number is displayed
					nMSB = MSB - 0xFF;
					nLSB = LSB - 0xFF - 0x01;
					curval = nMSB * 256 + nLSB; //store the most current value to curval
				}
				else
				{
					curval = MSB * 256 + LSB; //store the most current value to curval
				}
				if(preval == 0) //checks if the previous value is null
					preval = curval; //sets preval to the current value
				else
				{
					difval = abs(preval - curval); //stores the difference between the previous and current value
					if(difval > 512) //checks if the different value is too great
					{
						LSB = MSB;
						skipflag = 1;
					}
					else
						preval = curval; //sets the current value to preval
				}
				if(skipflag == 1) //checks if current bit needs to be skipped
				{
					skipflag = 0;
					secondnumber = 1;
					firstnumber = 0;
				}
				else
				{
					counter += 1; //add to counter
					fprintf(f, "%d %d \n", counter, curval); //print to file
				}
			}
			
		}
	//reset packet and header count
	packetcount = 0; 
	headercount = 0;
	loopcount += 1; //indicates end of packet has been reached
	}
};
/**************************************************************************************
 * This function is called from the main file. It opens the connection                *
 * between the Raspberry Pi and the Datex, setting all the relevant settings          *
 * to allow for serial communication. It then sends the request to the Datex          *
 * to begin the tranmission of data. The begindatacollection function is then         *
 * called, which polls the Datex for the time. Once this time is greater than         *
 * the time given by the user, the packetpull function is called. This function       *
 * takes the values from the Datex and inserts them into text documents. Once         *
 * the time in the packets are greater than the ending time, data colletion finishes. *
 * If repeat was selected, the collection process continues until it has looped the   *
 * amount of times equal to the amount value. The values are then printed to          *
 * the screen via GNUplot. Finally, a request is sent to cease data transmission.     *
 **************************************************************************************/
int datacollection(time_t starttime, time_t endtime, int repeat, int amount, int bednum, GtkWidget *status)
{
	byte commandflag = 0x7E; //flag used to let Datex know a command is being sent
	byte checksum; //sum of the total bytes sent
	
	
	GtkWidget *dialog = NULL;
	int fd0;
	fd0 = open( "/dev/ttyUSB0", O_RDWR | O_NOCTTY | O_NDELAY ); //open connection to Datex
	printf("%d \n", fd0);
	//error message if Datex not connected
	if(fd0 < 0) 
	{
		dialog = gtk_message_dialog_new(NULL, GTK_DIALOG_MODAL, GTK_MESSAGE_ERROR, GTK_BUTTONS_OK,
					"No connection to Datex. Please connect and run again.");
		gtk_dialog_run(GTK_DIALOG(dialog));
		gtk_widget_destroy(dialog);
		return;
	} 
	//serial options set to allow for communication
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

	options.c_cc[VTIME] = 0; // timer
	options.c_cc[VMIN] = 2; // blocks read until 2 chars received

	tcsetattr(fd0, TCSANOW, &options); //makes changes corresponding to the above parameters
	
	//create structs to be used for the request
	struct datex_hdr headerreq;
	struct datex_record requestPkt;
	struct wf_req *pRequest;

	//Clear the packet
	memset (&requestPkt, 0x00, sizeof(datex_record));
	
	//Fill the header
	requestPkt.hdr.r_len = sizeof(datex_hdr) + sizeof(struct wf_req); //length
	requestPkt.hdr.r_maintype = 1; //main type of the record
	
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

	int checkr; //variable to check if data was read
	int checkw; //variable to check if data was written

	unsigned char const *structarray = (void *)&requestPkt;
	checksum = structarray[0];
	
	//Print request
	for(int i = 0; i < checksum; i++)
	{
		printf("%02x ", structarray[i]);
		if(i%20 == 0 && i!=0)
			printf("\n");
	}
	printf("\n");
	//Send command flag, request and finish flag to Datex
	write(fd0, (void *)&commandflag, 1);
	checkw = write(fd0, (void *)&requestPkt, checksum);
	write(fd0, (void *)&checksum, 1);
	write(fd0, (void *)&commandflag, 1);

	//Prints to screen that data collection will begin soon
	gtk_label_set_text(GTK_LABEL(status), "Preparing to start data collection, please wait.");
	while(gtk_events_pending())
		gtk_main_iteration_do(FALSE);
	
	begindatacollection(starttime, fd0); //run function that polls for time of packet until packet time is greater than start time
	
	system("sudo mount -a"); //mount the USB drive to the Pi
	int timedif; //variable for the time difference between start and end time
	if(repeat == 1) //run if user has selected repeat
	{
		FILE * f[amount];
		for(int i = 0; i < amount; i++)
		{
			char filename[60];
			char statusname[50];
			struct tm starttimeinfo;
			struct tm endtimeinfo;
			starttimeinfo = *localtime(&starttime);
			endtimeinfo = *localtime(&endtime);
			char bufstart[80];
			strftime(bufstart, sizeof(bufstart), "%Y%m%d_%H%M%S", &starttimeinfo);
			char bufend[80];
			strftime(bufend, sizeof(bufend), "%Y%m%d_%H%M%S", &endtimeinfo);
			char correcttime[80];
			strftime(correcttime, sizeof(correcttime), "%Y/%m/%d %H:%M:%S", &starttimeinfo);
			sprintf(filename, "%s_BedNumber_%d.txt", bufstart, bednum);
			printf("%s \n", filename);
			sprintf(statusname, "Collecting data from %s to %s", bufstart, bufend);
			gtk_label_set_text(GTK_LABEL(status), statusname);
			while(gtk_events_pending())
				gtk_main_iteration_do(FALSE);
			f[i] = fopen(filename, "w");
			fprintf(f[i],"%s, Bed Number: %d, Length of Time: %d seconds\n", correcttime, bednum, (endtime - starttime)); //print header to file
			if(f[i]==NULL)
			{
				gtk_label_set_text(GTK_LABEL(status), "Unable to open file. Please try data collection again.");
				while(gtk_events_pending())
					gtk_main_iteration_do(FALSE);
				return;
			}
			packetpull(starttime, endtime, fd0, f[i]);
			fclose(f[i]);
			char copystring[100];
			sprintf(copystring, "mv %s /home/pi/usb/", filename);
			system(copystring);
			timedif = endtime - starttime;
			printf("%d \n", timedif);
			starttime = endtime;
			endtime = endtime + timedif;
		}
	}
	else
	{
		FILE * f;
		char filename[20];
		char statusname[50];
		struct tm starttimeinfo;
		struct tm endtimeinfo;
		starttimeinfo = *localtime(&starttime);
		endtimeinfo = *localtime(&endtime);
		char bufstart[80];
		strftime(bufstart, sizeof(bufstart), "%Y%m%d_%H%M%S", &starttimeinfo);
		char bufend[80];
		strftime(bufend, sizeof(bufend), "%Y%m%d_%H%M%S", &endtimeinfo);
		char correcttime[80];
		strftime(correcttime, sizeof(correcttime), "%Y/%m/%d %H:%M:%S", &starttimeinfo);
		sprintf(filename, "%s_BedNumber_%d.txt", bufstart, bednum);
		sprintf(statusname, "Collecting data from %s to %s", bufstart, bufend);
		gtk_label_set_text(GTK_LABEL(status), statusname);
		while(gtk_events_pending())
			gtk_main_iteration_do(FALSE);
		f = fopen(filename, "w");
		fprintf(f,"%s, Bed Number: %d, Length of Time: %d seconds\n", correcttime, bednum, (endtime - starttime)); //print header to file
		packetpull(starttime, endtime, fd0, f);
		fclose(f);
		char copystring[100];
		sprintf(copystring, "mv %s /home/pi/usb/", filename);
		system(copystring);
	}
	system("sudo umount -a");
	
	gtk_label_set_text(GTK_LABEL(status), "Finished Collecting Data");
		while(gtk_events_pending())
			gtk_main_iteration_do(FALSE);
	
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
	
	//Send command flag, request and finish flag to Datex
	write(fd0, (void *)&commandflag, 1);
	checkw = write(fd0, (void *)&requestPkt, checksum);
	write(fd0, (void *)&checksum, 1);
	write(fd0, (void *)&commandflag, 1);
	
	return 0;
};


