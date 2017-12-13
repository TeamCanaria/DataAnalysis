/*******************************************************
 * Defines the structs needed to send requests		   *
 * to the Datex machine, as stated in the user manual. *
 *******************************************************/
 
typedef unsigned long dword;
typedef unsigned short word;
typedef unsigned int uniint32;
typedef unsigned char byte;

typedef struct __attribute__((__packed__)) sr_desc
{
	short 		sr_offset; //relative pointer to the subrecord
	byte		sr_type; //subrecord type
}sr_desc;

typedef struct __attribute__((__packed__)) datex_hdr
{
	short 		r_len; //total length of the record
	byte 		r_nbr; //record number
	byte 		dri_level; //interface level, see pg 6
	word		plug_id; //plug identified number of the sending monitor
	dword 		r_time; //time when record was transmitted
	byte 		reserved1;
	byte		reserved2;
	word 		reserved3;
	short 		r_maintype; //main type of the record (DRI_MT_WAVE = 1 for waveform)
	struct 		sr_desc sr_desc[8]; //array that describes the subrecord types
}datex_hdr;

typedef struct wf_hdr
{
	short 		act_len; //the number of 16-bit waveform samples in the subrecord
	word 		status; //handled as bitfield, pg 73, says if a sample is missed
	word		reserved; //reserved
}wf_hdr;


typedef struct __attribute__((__packed__)) wf_req
{	
	short req_type; //0 = continuous transmission (WF_REQ_CONT_START)
					//1 = stop transmission (WF_REQ_CONT_STOP)
	short res; //set to 0 maybe
	byte type[8]; //set to 0 maybe
	short reserved[10]; //array of requested waveform subrecords
}wf_req;

typedef struct __attribute__((__packed__)) dri_phdb
{
	dword time; //time stamp of the record in unix time
	union
	{
		/*struct basic_phdb basic;
		struct ext1_phdb ext1;
		struct ext2_phdb ext2;
		struct ext3_phdb ext3;*/
	} physdata;
	byte marker; //contains the number of the latest entered mark
	byte reserved;
	word cl_drilvl_subt;
}driphdb;

typedef struct __attribute__((__packed__)) dri_phdb_req
{
	byte phdb_rcrd_type;
	short tx_ival;
	long phdb_class_bf;
	short reserved;
}dri_phdb_req;

union ph_srcrds
{
	byte ph_subrec[5 * sizeof(struct dri_phdb)];
}ph_srcrds;
	
union wf_srcrds
{
	short *data; 
}wf_srcrds;

typedef struct datex_record
{
	struct datex_hdr hdr; //header info of the data
	union
	{
		union wf_srcrds wf_rcrd; //waveform application data interface
		union ph_srcrds ph_rcrd; //physiological data and trend download application data interface
	//	union al_srcrds al_rcrd; //alarm transmission application data interface
	//	union nw_srcrds nw_rcrd; //not needed
	//	union fo_srcrds fo_rcrd; //not needed
		unsigned char 	data[1450]; //maximum record size
	} rcrd;
}datex_record;
