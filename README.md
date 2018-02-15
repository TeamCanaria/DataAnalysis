# Data Analysis

Canaria's scripts for collecting, signal processing and analysing HRV data in Python. This includes processing data collected from [Arduino Nano](https://github.com/TeamCanaria/Prototype) from the Prototype repository, through serial and through bluetooth, and extracting heart rate, HRV measures and SpO2 from the data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Install commands are provided in the following links

>1. Download and install [Jupyter Notebooks](https://jupyter.org/install.html)
>2. Get familiar with iPython notebooks and Jupyter [here](https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook)
>3. Python libraries required are [pySerial](https://github.com/pyserial/pyserial),  [PyBluez](https://github.com/karulis/pybluez) and [AWS SDK for Python](https://aws.amazon.com/sdk-for-python/)

### Installing

## Collecting data

Once the prerequisites are installed, we can start to walkthrough the different data science tools available to us.

GCUH has provided some C code that supposedly will have a Raspberry Pi receive data from ICU equipment and process it in a GUI software. These scripts are contained in the DatexCollectionSoftware/ and DatexPi/ directories but due to compile errors, we haven't been able to see it in action.

```
gcc `pkg-config --cflags --libs gtk+-2.0` main.c -o DatexConnectionSoftware
```

We also have two other methods of collecting our data: through bluetooth sockets and through serial port. For now we will be testing our prototype using serial interface, but bluetooth is always on option for the future.

### Running the bluetooth example

Import the `bluetooth` module and run the `discover_devices()` routine

```python
import bluetooth
from bluetooth import *

# Find nearby devices
print "looking for nearby devices..."
nearby_devices = bluetooth.discover_devices(lookup_names = True, flush_cache = True, duration = 20)
print "found %d devices" % len(nearby_devices)
```

`discover_devices()` will return a list of nearby devices detected and doesn't require any arguments.

Full documentation of Bluetooth programming can be found [here](https://people.csail.mit.edu/albert/bluez-intro/index.html)

### Running the software that connects through serial and uploads to AWS cloud

The Python notebook where our attention is at the most right now is the `connect_aws.ipynb` notebook.

By default, the port on Linux OS and Raspbian would be in /dev/ttyUSB0 and on Windows, check Device Manager for the specific COM port.

```python
# Read from the serial
try:
    read_serial = serial.Serial("/dev/ttyUSB0", 250000, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS) # 115200 is the serial number in Arduino code
                                                      # dev/ttyUSB0 is the port number optain from ls/dev/tty*
except:
    read_serial = serial.Serial("/dev/ttyUSB1", 250000, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
```

Once communication between the hardware and software has been established we create a .csv file documented by the date

```python
# Create file name which match the date
current_time = datetime.now()
file_name = current_time.strftime("%Y-%m-%d") + '.csv'
```

We can then define a function for writing column headers, print_first_line(written_file) which takes a write-only file as an argument, and a function for checking whether to create a new file or to edit an existing file, check_file_exist(file_name).

```python
def print_first_line(written_file):
    written_file.write('red,amb1,ir,amb2,green\n')
    return written_file

def check_file_exist(file_name):
    if file_name not in os.listdir(os.curdir):
        # File does not exist, create new file
        written_file = open(file_name, "w")
        written_file = print_first_line(written_file)
    else:
        # File already exist, append new rows
        written_file = open(file_name, "a")
    return written_file
```

Writing the data locally depends entirely on how you prefer to format it and send it through. Python will interpret incoming bytes as hexadecimal in the format b'\xff\xff' so play around with the int(), encode() and decode() functions in order to format according to your preference of representing the data.

## Processing the data

Paul Van Gent's HRV analysis tutorial is a great introduction to DSP applied to heart rate data, learn more [here](https://github.com/paulvangentcom/heartrate_analysis_python). The basic idea is to read the .csv file using pandas and visualise the data using matplotlib.

```python
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv('2018-01-30.csv') #read heart rate data from its csv file

plt.title('Heart Rate Signal') #the title of our heart rate plot
plt.ylim(24000, 26500)
plt.xlim(18750, 19500)
plt.plot(dataset['Red Signal']) #draw the plot object
plt.show() #display the plot object
```

This will output:

![signal](https://github.com/TeamCanaria/DataAnalysis/blob/master/images/signal1.png)

### Analysis and testing

All the steps and code provided in the Van Gent Tutorial have been modified to meet our own needs, are laid out in `ECG_connect_and_analyse.ipynb`. The name is misleading, it's actually meant to be PPG. Meg McConnell, a PhD student from GCUH, has provided scripts of her work in progress for us which we can look at for reference.   

The HRV measures that we extract from the data are easily calculated using the following functions on the list containing all the RR intervals

```
ibi = np.mean(RR_list) #Take the mean of RR_list to get the mean Inter Beat Interval
print("IBI:", ibi)

sdnn = np.std(RR_list) #Take standard deviation of all R-R intervals
print("SDNN:", sdnn)

sdsd = np.std(RR_diff) #Take standard deviation of the differences between all subsequent R-R intervals
print("SDSD:", sdsd)

rmssd = np.sqrt(np.mean(RR_sqdiff)) #Take root of the mean of the list of squared differences
print("RMSSD:", rmssd)
```
