/***************************************************************
 * Header containining various functions from the program.	   *
 * Includes unix time conversion and array printing functions. *
 ***************************************************************/

/**********************************************
 * Prints actual time from a given unix time. *
 **********************************************/
void unixtime(time_t packet_time)
{
	struct tm timeinfo;
	timeinfo = *localtime(&packet_time);
	char buf[80];
    strftime(buf, sizeof(buf), "%a %Y-%m-%d %H:%M:%S %Z", &timeinfo);
    printf("%s\n", buf);    
};

/**************************
 * Prints a memory array. *
 **************************/
void print_mem(void const *vp, size_t n)
{
    unsigned char const *p = vp;
    for (size_t i=0; i<n; i++)
        printf("%02x\n", p[i]);
    putchar('\n');
};


/********************************************************************
 * Converts the time given from the GUI to unix time, to allow for  *
 * comparison with the time received in the packets from the Datex. *
 * Returns a time_t unix time value of the starting time of data    *
 * collection. 														*
 ********************************************************************/
time_t datacollectionstart(int startyear, int startmonth, int startday, int starthr, int startmin)
{
	struct tm start;
	time_t t;
	
	start.tm_sec = 0;
	start.tm_min = startmin;
	start.tm_hour = starthr;
	start.tm_mday = startday;
	start.tm_mon = startmonth - 1;
	start.tm_year = startyear - 1900;
	start.tm_isdst = 0;
	start.tm_zone = "GMT";
	t = mktime (&start);
	printf("%s \n", asctime(&start));
	
	printf("%d \n", t);
	return t;
};

/********************************************************************
 * Converts the time given from the GUI to unix time, to allow for  *
 * comparison with the time received in the packets from the Datex. *
 * Returns a time_t unix time value of the ending time of data      *
 * collection. 														*
 ********************************************************************/
time_t datacollectionend(int startyear, int startmonth, int startday, int starthr, int startmin,
					int lengthhr, int lengthmin)
{
	struct tm end;
	time_t t;
	
	end.tm_sec = 0;
	end.tm_min = startmin + lengthmin;
	end.tm_hour = starthr + lengthhr;
	end.tm_mday = startday;
	end.tm_mon = startmonth - 1;
	end.tm_year = startyear - 1900;
	end.tm_isdst = 0;
	end.tm_zone = "GMT";
	t = mktime (&end);
	printf("%s \n", asctime(&end));
	
	printf("%d \n", t);
	return t;
};
