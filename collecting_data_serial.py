import serial                              # Python library to read data from Raspberry Pi serial 
from datetime import datetime, timedelta   # Python library to check datetime
import os                                  # Python library to use operating system dependent functionality
import boto3 			           # Python library to connect aws servers
import botocore			           # Python library to handle message from aws

# Read from the serial,
print("Establish USB Serial Connection")
try:
    read_serial = serial.Serial("/dev/ttyUSB0", 115200) # 115200 is the serial number in Arduino code
                                                        # dev/ttyUSB0 and dev/ttyUSB1 is the port number optain from ls/dev/tty*
except:
    read_serial = serial.Serial("/dev/ttyUSB1", 115200)

# Connect with s3 Service
print("Connect with s3 Service")
BUCKET_NAME = 'canaria-client-data'
session = boto3.Session(profile_name='default') # take secret key in awscli credentials file.
s3_client = session.client('s3')

# Create file name which match the date
current_time = datetime.now()
file_name = current_time.strftime("%Y-%m-%d") + '.csv'
board_no = 'board_4'
print(file_name)
user = raw_input("Input User's Name:")
user = board_no + '/' + user

# Create columns for the data file
def print_first_line(written_file):
    written_file.write('Date,')
    written_file.write('Patient_ID,')
    written_file.write('Red_Signal,')
    written_file.write('State')
    written_file.write('\n')
    return written_file

# Check file already exist in local machine
def check_file_exist(file_name):
    if file_name not in os.listdir(os.curdir):
        # File does not exist, create new file
        written_file = open(file_name, "w")
        written_file = print_first_line(written_file)
    else:
        # File already exist, append new rows
        written_file = open(file_name, "a")
    return written_file

def exist_file_from_s3(file_name, user, bucket_name, s3_client):
    exist_file = 0
    for key in s3_client.list_objects(Bucket=bucket_name)['Contents']:
        if key['Key'] == (user+'/'+file_name):
            print('Found file in the s3 backet')
            s3_client.download_file(bucket_name, user+'/' + file_name, file_name)
	    print('downloading file...')
            print('opening the file...')
            exist_file = open(file_name, "a")
            break
    if exist_file == 0:
	print('File is not in the s3 backet')
        print('Making file...')
        exist_file = check_file_exist(file_name)
    return exist_file

# Updating the data on s3 backet 
def update_file_signal(file_write, file_name, user, bucket_name, s3_client):
    file_write.close()                                       # Close the file for uploading
    try:
    	print('Uploading Data')
    	s3_client.upload_file(file_name, bucket_name, user+'/'+ file_name)     # Uploadfile to s3
    except botocore.exceptions.ClientError:
	print('Upload Fail')
    	file_write = open(file_write.name, "a")                   # Reopen close file
    file_write = open(file_write.name, "a")
    return file_write


# Upload file to s3 every a duration of time
update_time = 10           # duration how often the s3 be updated
state = 'N'				   # state of patient: N for normal, F for fatigue 
print('Creating file csv')
file_signal = exist_file_from_s3(file_name, user, BUCKET_NAME, s3_client)
update_flag = datetime.now() + timedelta(minutes = update_time)
print("Read data from Serial")
try: 
    while 1:
        data = read_serial.readline()  # Data from serial separate by newline character
        data = data.strip()            # Remove newline character of Arduino IDE
	if not(data.isdigit()):		   # Check signal is integer weird characters which generate from arduino
	    if data == 'F':			   # If signal is F meaning that patient is fatigue
	        state = 'F'
		continue
	    else:
		continue 

        file_signal.write(datetime.now().strftime("%H:%M:%S.%f") + ",")    # Record time corresponding to the signal 
        file_signal.write(user + ",")    # Write to column Patient Id
        file_signal.write(data)
	print(data+','+state)
        file_signal.write("\n")
        
	# Time to update s3
        if datetime.now() >= update_flag:         # Update the file
            file_signal = update_file_signal(file_signal, file_name, user, BUCKET_NAME, s3_client)
            update_flag = datetime.now() + timedelta(minutes = update_time)
        # New day, program create new data file
	if (current_time.day != datetime.now().day) or (current_time.month != datetime.now().month) \
	or (current_time.year != datetime.now().year):
            file_signal = update_file_signal(file_signal, file_name, user, BUCKET_NAME, s3_client)
	    current_time = datetime.now()
	    file_name = current_time.strftime("%Y-%m-%d") + '.csv'
	    file_signal = exist_file_from_s3(file_name, user, BUCKET_NAME, s3_client)
	    update_flag = datetime.now() + timedelta(minutes = update_time)
 
except KeyboardInterrupt:
    file_signal.close()
    print("End")
