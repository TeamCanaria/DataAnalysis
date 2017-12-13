/**********************************************************
 * The main file for the program. This will need		  *	
 * to be compiled to create an output. It contains		  *
 * all the GUI elements of the software. When a user      *
 * has input all the values they want to the GUI, it      *
 * turns those index numbers to useable integers, which   *
 * are then sent to the datacollectionfunc.h to start     *
 * the data collection.								 	  *
 **********************************************************/

#include <gtk/gtk.h>
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
#include <tgmath.h>
#include "func.h"
#include "structdef.h"
#include "datacollectionfunc.h"

#define PRINT_OPAQUE_STRUCT(p)  print_mem((p), sizeof(*(p)))

typedef unsigned long dword;
typedef unsigned short word;
typedef unsigned int uniint32;
typedef unsigned char byte;

/************************************************************
 * Struct created to hold the index and integer values of   *
 * the GUI. The struct is necessary as GTK button functions *
 * only allow for a single variable.                        *
 ************************************************************/
struct datexstruct
{
	GtkWidget *starthrcom;
	GtkWidget *startmincom;
	GtkWidget *startdaycom;
	GtkWidget *startmonthcom;
	GtkWidget *startyearcom;
	GtkWidget *lengthhrcom;
	GtkWidget *lengthmincom;
	GtkWidget *repeatcom;
	GtkWidget *amountcom;
	GtkWidget *bednumcom;
	GtkWidget *status;
	int starthr;
	int startmin;
	int startday;
	int startmonth;
	int startyear;
	int lengthhr;
	int lengthmin;
	int repeat;
	int amount;
	int bednum;
};

/*******************************************************************
 * Function to convert index variables from the GUI into integers  *
 * which are then sent to datacollectionfunc.h to begin collecting *
 * the data from the ECG.										   *
 *******************************************************************/
void collectdata(GtkWidget *widget, struct datexstruct *datex)
{
	//Starting Day Variable Setting
	switch(gtk_combo_box_get_active(GTK_COMBO_BOX(datex->startdaycom)))
	{
		case 0: datex->startday = 1; break;
		case 1: datex->startday = 2; break;
		case 2: datex->startday = 3; break;
		case 3: datex->startday = 4; break;
		case 4: datex->startday = 5; break;
		case 5: datex->startday = 6; break;
		case 6: datex->startday = 7; break;
		case 7: datex->startday = 8; break;
		case 8: datex->startday = 9; break;
		case 9: datex->startday = 10; break;
		case 10: datex->startday = 11; break;
		case 11: datex->startday = 12; break;
		case 12: datex->startday = 13; break;
		case 13: datex->startday = 14; break;
		case 14: datex->startday = 15; break;
		case 15: datex->startday = 16; break;
		case 16: datex->startday = 17; break;
		case 17: datex->startday = 18; break;
		case 18: datex->startday = 19; break;
		case 19: datex->startday = 20; break;
		case 20: datex->startday = 21; break;
		case 21: datex->startday = 22; break;
		case 22: datex->startday = 23; break;
		case 23: datex->startday = 24; break;
		case 24: datex->startday = 25; break;
		case 25: datex->startday = 26; break;
		case 26: datex->startday = 27; break;
		case 27: datex->startday = 28; break;
		case 28: datex->startday = 29; break;
		case 29: datex->startday = 30; break;
		case 30: datex->startday = 31; break;
	}
	//Starting Month Variable Setting
	switch(gtk_combo_box_get_active(GTK_COMBO_BOX(datex->startmonthcom)))
	{
		case 0: datex->startmonth = 1; break;
		case 1: datex->startmonth = 2; break;
		case 2: datex->startmonth = 3; break;
		case 3: datex->startmonth = 4; break;
		case 4: datex->startmonth = 5; break;
		case 5: datex->startmonth = 6; break;
		case 6: datex->startmonth = 7; break;
		case 7: datex->startmonth = 8; break;
		case 8: datex->startmonth = 9; break;
		case 9: datex->startmonth = 10; break;
		case 10: datex->startmonth = 11; break;
		case 11: datex->startmonth = 12; break;
	}
	//Starting Year Variable Setting
	switch(gtk_combo_box_get_active(GTK_COMBO_BOX(datex->startyearcom)))
	{
		case 0: datex->startyear = 2016; break;
		case 1: datex->startyear = 2017; break;
		case 2: datex->startyear = 2018; break;
		case 3: datex->startyear = 2019; break;
		case 4: datex->startyear = 2020; break;
		case 5: datex->startyear = 2021; break;
		case 6: datex->startyear = 2022; break;
		case 7: datex->startyear = 2023; break;
		case 8: datex->startyear = 2024; break;
	}
	//Starting Hour Variable Setting
	switch(gtk_combo_box_get_active(GTK_COMBO_BOX(datex->starthrcom)))
	{
		case 0: datex->starthr = 0; break;
		case 1: datex->starthr = 1; break;
		case 2: datex->starthr = 2; break;
		case 3: datex->starthr = 3; break;
		case 4: datex->starthr = 4; break;
		case 5: datex->starthr = 5; break;
		case 6: datex->starthr = 6; break;
		case 7: datex->starthr = 7; break;
		case 8: datex->starthr = 8; break;
		case 9: datex->starthr = 9; break;
		case 10: datex->starthr = 10; break;
		case 11: datex->starthr = 11; break;
		case 12: datex->starthr = 12; break;
		case 13: datex->starthr = 13; break;
		case 14: datex->starthr = 14; break;
		case 15: datex->starthr = 15; break;
		case 16: datex->starthr = 16; break;
		case 17: datex->starthr = 17; break;
		case 18: datex->starthr = 18; break;
		case 19: datex->starthr = 19; break;
		case 20: datex->starthr = 20; break;
		case 21: datex->starthr = 21; break;
		case 22: datex->starthr = 22; break;
		case 23: datex->starthr = 23; break;
	}
	//Starting Minute Variable Setting
	switch(gtk_combo_box_get_active(GTK_COMBO_BOX(datex->startmincom)))
	{
		case 0: datex->startmin = 0; break;
		case 1: datex->startmin = 5; break;
		case 2: datex->startmin = 10; break;
		case 3: datex->startmin = 15; break;
		case 4: datex->startmin = 20; break;
		case 5: datex->startmin = 25; break;
		case 6: datex->startmin = 30; break;
		case 7: datex->startmin = 35; break;
		case 8: datex->startmin = 40; break;
		case 9: datex->startmin = 45; break;
		case 10: datex->startmin = 50; break;
		case 11: datex->startmin = 55; break;
	}
	//Hour Length Variable Setting
	switch(gtk_combo_box_get_active(GTK_COMBO_BOX(datex->lengthhrcom)))
	{
		case 0: datex->lengthhr = 0; break;
		case 1: datex->lengthhr = 1; break;
		case 2: datex->lengthhr = 2; break;
		case 3: datex->lengthhr = 3; break;
		case 4: datex->lengthhr = 4; break;
		case 5: datex->lengthhr = 5; break;
		case 6: datex->lengthhr = 6; break;
		case 7: datex->lengthhr = 7; break;
		case 8: datex->lengthhr = 8; break;
		case 9: datex->lengthhr = 9; break;
		case 10: datex->lengthhr = 10; break;
		case 11: datex->lengthhr = 11; break;
		case 12: datex->lengthhr = 12; break;
		case 13: datex->lengthhr = 13; break;
		case 14: datex->lengthhr = 14; break;
		case 15: datex->lengthhr = 15; break;
		case 16: datex->lengthhr = 16; break;
		case 17: datex->lengthhr = 17; break;
		case 18: datex->lengthhr = 18; break;
		case 19: datex->lengthhr = 19; break;
		case 20: datex->lengthhr = 20; break;
		case 21: datex->lengthhr = 21; break;
		case 22: datex->lengthhr = 22; break;
		case 23: datex->lengthhr = 23; break;	
	}
	//Minute Length Variable Setting
	switch(gtk_combo_box_get_active(GTK_COMBO_BOX(datex->lengthmincom)))
	{
		case 0: datex->lengthmin = 0; break;
		case 1: datex->lengthmin = 5; break;
		case 2: datex->lengthmin = 10; break;
		case 3: datex->lengthmin = 15; break;
		case 4: datex->lengthmin = 20; break;
		case 5: datex->lengthmin = 25; break;
		case 6: datex->lengthmin = 30; break;
		case 7: datex->lengthmin = 35; break;
		case 8: datex->lengthmin = 40; break;
		case 9: datex->lengthmin = 45; break;
		case 10: datex->lengthmin = 50; break;
		case 11: datex->lengthmin = 55; break;
	}
	//Repeat Flag Setting
	switch(gtk_combo_box_get_active(GTK_COMBO_BOX(datex->repeatcom)))
	{
		case 0: datex->repeat = 1; break;
		case 1: datex->repeat = 0; break;
	}
	//Amount of Repeat Times Variable Setting
	/*switch(gtk_combo_box_get_active(GTK_COMBO_BOX(datex->amountcom)))
	{
		case 0: datex->amount = 1; break;
		case 1: datex->amount = 2; break;
		case 2: datex->amount = 3; break;
		case 3: datex->amount = 4; break;
		case 4: datex->amount = 0; break;
		
	}*/
	datex->amount = gtk_combo_box_get_active(GTK_COMBO_BOX(datex->amountcom)) + 1;
	//Bed number of patient Variable Setting
	/*switch(gtk_combo_box_get_active(GTK_COMBO_BOX(datex->bednumcom)))
	{
		case 0: datex->bednum = 1; break;
		case 1: datex->bednum = 2; break;
		case 2: datex->bednum = 3; break;
		case 3: datex->bednum = 4; break;
		case 4: datex->bednum = 5; break;
		case 5: datex->bednum = 6; break;
		case 6: datex->bednum = 7; break;
		case 7: datex->bednum = 8; break;
		case 8: datex->bednum = 9; break;
		case 9: datex->bednum = 10; break;
	}*/
	datex->bednum = gtk_combo_box_get_active(GTK_COMBO_BOX(datex->bednumcom)) + 1;
	//creating time objects to allow of unix time conversions and comparisons
	time_t starttimeunix;
	time_t endtimeunix;
	//functions to determine the unix time of the start and end times found in func.h
	starttimeunix = datacollectionstart(datex->startyear, datex->startmonth, datex->startday, datex->starthr, 
					datex->startmin);
	endtimeunix = datacollectionend(datex->startyear, datex->startmonth, datex->startday, datex->starthr, 
					datex->startmin, datex->lengthhr, datex->lengthmin);
	//data collection function found in datacollectionfunc.h
	datacollection(starttimeunix, endtimeunix, datex->repeat, datex->amount, datex->bednum, datex->status);
};

/**************************************************************
 * Main function of the program. This creates all the objects *
 * necessary to build the GUI for the program.				  *
 **************************************************************/
int main (int argc, char *argv[])
{
    GtkWidget *maintable = NULL;
    GtkWidget *mainwindow = NULL;

    //widgets
    GtkWidget *starthrentry = NULL;
    GtkWidget *startminentry = NULL;
    GtkWidget *startyearentry = NULL;
    GtkWidget *startmonthentry = NULL;
    GtkWidget *startdayentry = NULL;
    GtkWidget *lengthhrentry = NULL;
    GtkWidget *lengthminentry = NULL;
    GtkWidget *repeatentry = NULL;
	GtkWidget *amountentry = NULL;
	GtkWidget *bednumentry = NULL;
	GtkWidget *gobutton = NULL;
	GtkWidget *haltbutton = NULL;
	
	//labels
    GtkWidget *startdatelabel = NULL;
    GtkWidget *starttimelabel = NULL;
    GtkWidget *lengthlabel = NULL;
    GtkWidget *repeatlabel = NULL;
    GtkWidget *amountlabel = NULL;
    GtkWidget *bednumlabel = NULL;
    GtkWidget *golabel = NULL;
    GtkWidget *haltlabel = NULL;
    GtkWidget *statuslabel = NULL;
	
	//initialise struct
	struct datexstruct *datex = malloc(sizeof(*datex));
	
	//initialise GTK+
    g_log_set_handler ("Gtk", G_LOG_LEVEL_WARNING, (GLogFunc) gtk_false, NULL);
    gtk_init (&argc, &argv);
    g_log_set_handler ("Gtk", G_LOG_LEVEL_WARNING, g_log_default_handler, NULL);
    
    //initialise labels
    startdatelabel = gtk_label_new("Start Date (day/month/year)");
    starttimelabel = gtk_label_new("Start Time (hour/min)");
    lengthlabel = gtk_label_new("Length of Time (hour/min)");
    repeatlabel = gtk_label_new("Repeat Sequence");
    amountlabel = gtk_label_new("Number of Times");
    bednumlabel = gtk_label_new("Bed Number");
    golabel = gtk_label_new("Go");
    haltlabel = gtk_label_new("Halt");
    statuslabel = gtk_label_new("Waiting to begin data collection...");
    datex->status = statuslabel;
    
	//fill start hour combo box with values
    starthrentry = gtk_combo_box_new_text();
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "00");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "01");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "02");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "03");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "04");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "05");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "06");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "07");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "08");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "09");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "10");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "11");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "12");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "13");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "14");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "15");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "16");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "17");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "18");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "19");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "20");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "21");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "22");
    gtk_combo_box_append_text(GTK_COMBO_BOX(starthrentry), "23");
    datex->starthrcom = starthrentry;
    
	//fill start minute combo box with values
    startminentry = gtk_combo_box_new_text();
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "00");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "05");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "10");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "15");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "20");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "25");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "30");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "35");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "40");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "45");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "50");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startminentry), "55");
    datex->startmincom = startminentry;
    
	//fill start year combo box with values
    startyearentry = gtk_combo_box_new_text();
    gtk_combo_box_append_text(GTK_COMBO_BOX(startyearentry), "2016");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startyearentry), "2017");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startyearentry), "2018");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startyearentry), "2019");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startyearentry), "2020");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startyearentry), "2021");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startyearentry), "2022");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startyearentry), "2023");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startyearentry), "2024");
    datex->startyearcom = startyearentry;
    
	//fill start month combo box with values
    startmonthentry = gtk_combo_box_new_text();
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "Jan");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "Feb");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "Mar");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "Apr");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "May");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "Jun");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "Jul");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "Aug");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "Sep");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "Oct");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "Nov");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startmonthentry), "Dec");
    datex->startmonthcom = startmonthentry;
    
	//fill start day combo box with values
    startdayentry = gtk_combo_box_new_text();
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "1");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "2");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "3");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "4");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "5");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "6");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "7");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "8");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "9");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "10");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "11");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "12");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "13");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "14");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "15");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "16");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "17");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "18");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "19");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "20");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "21");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "22");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "23");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "24");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "25");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "26");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "27");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "28");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "29");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "30");
    gtk_combo_box_append_text(GTK_COMBO_BOX(startdayentry), "31");
    datex->startdaycom = startdayentry;
    
	//fill length hour combo box with values
    lengthhrentry = gtk_combo_box_new_text();
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "0 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "1 hour");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "2 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "3 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "4 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "5 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "6 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "7 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "8 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "9 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "10 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "11 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "12 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "13 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "14 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "15 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "16 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "17 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "18 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "19 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "20 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "21 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "22 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "23 hours");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthhrentry), "24 hours");
    datex->lengthhrcom = lengthhrentry;
    
	//fill length minute combo box with values
    lengthminentry = gtk_combo_box_new_text();
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "0 minutes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "5 minutes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "10 minutes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "15 minutes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "20 minutes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "25 minutes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "30 minutes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "35 minutes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "40 minutes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "45 minutes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "50 minutes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(lengthminentry), "55 minutes");
    datex->lengthmincom = lengthminentry;
    
	//fill repeat combo box with values
    repeatentry = gtk_combo_box_new_text();
    gtk_combo_box_append_text(GTK_COMBO_BOX(repeatentry), "Yes");
    gtk_combo_box_append_text(GTK_COMBO_BOX(repeatentry), "No");
    datex->repeatcom = repeatentry; 
    
	//fill amount combo box with values
	amountentry = gtk_combo_box_new_text();
	for(int i = 1; i <= 10; i++)
	{
		char str[3];
		sprintf(str, "%d", i);
		gtk_combo_box_append_text(GTK_COMBO_BOX(amountentry), str);
	}
	datex->amountcom = amountentry;
	
	//fill bed number combo box with values
	bednumentry = gtk_combo_box_new_text();
	for(int i = 1; i <= 500; i++)
	{
		char str[3];
		sprintf(str, "%d", i);
		gtk_combo_box_append_text(GTK_COMBO_BOX(bednumentry), str);
	}
	datex->bednumcom = bednumentry;
	
	//add labels to the buttons
	gobutton = gtk_button_new_with_label("Go");
	haltbutton = gtk_button_new_with_label("Halt");
	
	//create main window and table
	maintable = gtk_table_new(7 ,6, TRUE);
    mainwindow = gtk_window_new (GTK_WINDOW_TOPLEVEL);
    gtk_container_set_border_width (GTK_CONTAINER (mainwindow), 9);
    gtk_window_set_default_size(GTK_WINDOW(mainwindow), -1, -1);
    gtk_window_set_title (GTK_WINDOW (mainwindow), "DATEX ECG Data Logger");
    gtk_window_set_position (GTK_WINDOW (mainwindow), GTK_WIN_POS_CENTER);
    gtk_widget_realize (mainwindow);
    g_signal_connect (mainwindow, "destroy", gtk_main_quit, NULL);
    gtk_container_add (GTK_CONTAINER(mainwindow), maintable);
    
    //attach entries to main table
    gtk_table_attach(GTK_TABLE(maintable), startdatelabel, 0, 3, 0, 1,
          GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), starttimelabel, 3, 5, 0, 1,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), lengthlabel, 5, 7, 0, 1,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), startdayentry, 0, 1, 1, 2,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
   	gtk_table_attach(GTK_TABLE(maintable), startmonthentry, 1, 2, 1, 2,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), startyearentry, 2, 3, 1, 2,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), starthrentry, 3, 4, 1, 2,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
   	gtk_table_attach(GTK_TABLE(maintable), startminentry, 4, 5, 1, 2,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
	gtk_table_attach(GTK_TABLE(maintable), lengthhrentry, 5, 6, 1, 2,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), lengthminentry, 6, 7, 1, 2,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
	gtk_table_attach(GTK_TABLE(maintable), repeatlabel, 0, 2, 2, 3,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), amountlabel, 2, 4, 2, 3,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), bednumlabel, 5, 7, 2, 3,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), repeatentry, 0, 2, 3, 4,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), amountentry, 2, 4, 3, 4,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), bednumentry, 5, 7, 3, 4,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), statuslabel, 0, 4, 5, 6,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), gobutton, 5, 6, 5, 6,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    gtk_table_attach(GTK_TABLE(maintable), haltbutton, 6, 7, 5, 6,
                   GTK_FILL | GTK_SHRINK | GTK_EXPAND, GTK_FILL | GTK_SHRINK, 5, 5);
    
	//create path to function from go button
    g_signal_connect(gobutton, "clicked", G_CALLBACK(collectdata), (gpointer)datex);
   // g_signal_disconnect(haltbutton, 
	//show all the widgets
    gtk_widget_show_all (mainwindow);
    gtk_main ();
}
