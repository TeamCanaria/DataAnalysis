#all following code, excluding modifications where applicable, has been sourced under GNU 3.0 license from
#van Gent, P. (2016). Analyzing a Discrete Heart Rate Signal Using Python. 
#A tech blog about fun things with Python and embedded electronics. 
#Retrieved from: http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-heart-rate-signal-using-python-part-1/
#see also parts 2 and 3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

dataset = pd.read_csv('Vu2018_01_25EDIT.csv') #read heart rate data from its csv file

#calculate moving average with 0.75s in either direction, then append to dataset
hrw = 0.5 #1-sided window size, as proportion of the sampling frequency
samplingfreq = 100 #write a module to calculate this from the dataset later
mov_avg = pd.rolling_mean(dataset.RedSignal, window=int(hrw*samplingfreq)) #calculate the moving average

#impute where the moving average function returns NaN, which is the beginning of where x hrw
avg_hr = (np.mean(dataset.RedSignal))
mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]

mov_avg = [x*1.0 for x in mov_avg] #for now we raise the moving average by a % to prevent the T-peaks from interfering
#we will later do this dynamically
dataset['RedSignal_rollingmean'] = mov_avg #append the moving average to the dataset

#mark regions of interest
window = []
peaklist = []
listpos = 0 #use a counter to move between different data columns
for datapoint in dataset.RedSignal:
    rollingmean = dataset.RedSignal_rollingmean[listpos] #get the moving average
    if (datapoint <= rollingmean and len(window) < 1): #if there is no R-complex activity
        listpos += 1
        
    elif (datapoint > rollingmean): #if datapoint is above moving average, mark ROI
        window.append(datapoint)
        listpos += 1
    
    else: #if signal drops below local mean, determine highest point
        maximum = max(window)
        beatposition = listpos - len(window) + (window.index(max(window))) #note the point's x-coordinate
        peaklist.append(beatposition) #add detected peak to list
        window = [] #clear marked ROI
        listpos += 1
        
ybeat = [dataset.RedSignal[x] for x in peaklist] #get the y-value of all peaks for plotting purposes

RR_list = []
count = 0
while(count < (len(peaklist)-1)):
    RR_interval = (peaklist[count+1] - peaklist[count]) #calculate distance between each peak in sample
    ms_dist = ((RR_interval/samplingfreq) * 1000.0) #convert sample distances to ms distances
    RR_list.append(ms_dist) #append to ms distances list
    count += 1
    
bpm = 60000 / np.mean(RR_list) #60000ms (1 minute) / average R-R interval of signal
print("Average Heart Beat is: %.01f" %bpm) #round off to 1sf and print

plt.title('Detected peaks in signal')
plt.ylim(16550,17600)
plt.xlim(217400,217600)
plt.plot(dataset.RedSignal, alpha = 0.5, color = 'blue', label = "raw signal") #plot semi-transparent heart rate
plt.plot(mov_avg, color = 'green', label = "moving average") #plot the moving average
plt.scatter(peaklist, ybeat, color = 'red', label = "average: %.1f BPM" %bpm) #plot the peaks
plt.legend(loc = 4, framealpha = 0.6)
plt.scatter(peaklist, ybeat, color = 'red')
plt.show()