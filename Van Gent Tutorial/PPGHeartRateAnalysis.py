#all following code, excluding modifications where applicable, has been sourced under GNU 3.0 license from
#van Gent, P. (2016). Analyzing a Discrete Heart Rate Signal Using Python. 
#A tech blog about fun things with Python and embedded electronics. 
#Retrieved from: http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-heart-rate-signal-using-python-part-1/

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

measures = {}

def get_data(filename):
    dataset = pd.read_csv(filename)
    return dataset

def rolmean(dataset, hrw, samplingfreq):
    mov_avg = pd.rolling_mean(dataset.RedSignal, window=int(hrw*samplingfreq))
    avg_hr = (np.mean(dataset.RedSignal))
    mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
    #mov_avg = [x*1.2 for x in mov_avg] #we may raise the moving average by a % to reduce interference from diastolic peaks
    dataset['RedSignal_rollingmean'] = mov_avg
    
def detect_peaks(dataset):
    window = []
    peaklist = []
    listpos = 0
    for datapoint in dataset.RedSignal:
        rollingmean = dataset.RedSignal_rollingmean[listpos]
        if (datapoint < rollingmean) and (len(window) < 1):
            listpos += 1
        elif (datapoint > rollingmean):
            window.append(datapoint)
            listpos += 1
        else:
            maximum = max(window)
            beatposition = listpos - len(window) + (window.index(max(window)))                                     
            peaklist.append(beatposition)
            window = []
            listpos += 1
    measures['peaklist'] = peaklist
    measures['ybeat'] = [dataset.RedSignal[x] for x in peaklist]
    
def calc_RR(dataset, samplingfreq):
    RR_list =[]
    peaklist = measures['peaklist']
    cnt = 0
    while (cnt < (len(peaklist) - 1)):
        RR_interval = (peaklist[cnt+1] - peaklist[cnt])
        ms_dist = ((RR_interval / samplingfreq) * 1000.0)
        RR_list.append(ms_dist)
        cnt += 1
    
    RR_diff = []
    RR_sqdiff = []

    count = 0 #use to iterate over RR/SS measures
    while (count < len(RR_list)-1):
        RR_diff.append(abs((RR_list[count] - RR_list[count+1]))) #calculate absolute difference between successive RR intervals
        RR_sqdiff.append(math.pow(RR_list[count] - RR_list[count+1], 2)) #calculate the squared difference
        count += 1
        
    measures['RR_list'] = RR_list
    measures['RR_diff'] = RR_diff
    measures['RR_sqdiff'] = RR_sqdiff
    
def calc_bpm():
    RR_list = measures['RR_list']
    measures['bpm'] = 60000 / np.mean(RR_list)
        
#function to calculate the time series HRV measures
def calc_ts_measures():
    RR_list = measures['RR_list']
    RR_diff = measures['RR_diff']
    RR_sqdiff = measures['RR_sqdiff']
    measures['bpm'] = 60000 / np.mean(RR_list)
    measures['ibi'] = np.mean(RR_list)
    measures['sdnn'] = np.std(RR_list)
    measures['sdsd'] = np.std(RR_diff)
    measures['rmssd'] = np.sqrt(np.mean(RR_sqdiff))
    nn20 = [x for x in RR_diff if (x > 20)]
    nn50 = [x for x in RR_diff if (x > 50)]
    measures['nn20'] = nn20
    measures['nn50'] = nn50
    measures['pnn20'] = float(len(nn20)) / float(len(RR_diff))
    measures['pnn50'] = float(len(nn50)) / float(len(RR_diff))
    
def plotter(dataset, title):
    peaklist = measures['peaklist']
    ybeat = measures['ybeat']
    plt.title(title)
    plt.ylim(17000,20600)
    plt.xlim(5000,6000)
    plt.plot(dataset.RedSignal, alpha=0.5, color='blue', label='raw signal')
    plt.plot(dataset.RedSignal_rollingmean, color='green', label='moving average')
    plt.scatter(peaklist, ybeat, color='red', label='average: %.1f BPM' %measures['bpm'])
    plt.legend(loc=4, framealpha=0.6)
    plt.show()

#finally we write a wrapper function to call the whole analysis quickly
def process(dataset, hrw, samplingfreq): #hrw is the 1-sided window size
    rolmean(dataset, hrw, samplingfreq)
    detect_peaks(dataset)
    calc_RR(dataset, samplingfreq)
    calc_bpm()
    #calc_ts_measures()
    plotter(dataset, 'Detected peaks in signal')




''' the code below includes a dynamic moving average threshold function, but is commented out for now in favour of a previous
version without this function in the name of expediency re: demo for Rio Tinto exec on Monday 29th Jan 2018

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

measures = {}

def get_data(filename):
    dataset = pd.read_csv(filename)
    return dataset

def rolmean(dataset, hrw, samplingfreq):
    mov_avg = pd.rolling_mean(dataset.RedSignal, window=int(hrw*samplingfreq))
    avg_hr = (np.mean(dataset.RedSignal))
    mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
    #mov_avg = [x*1.2 for x in mov_avg]
    dataset['RedSignal_rollingmean'] = mov_avg
    
def detect_peaks(dataset, ma_perc, samplingfreq): #Change the function to accept a moving average percentage 'ma_perc' argument
    rolmean = [(x+((x/100)*ma_perc)) for x in dataset.RedSignal_rollingmean] #Raise moving average with passed ma_perc
    window = []
    peaklist = []
    listpos = 0 
    for datapoint in dataset.RedSignal:
        rollingmean = rolmean[listpos]
        if (datapoint <= rollingmean) and (len(window) <= 1): #Here is the update in (datapoint <= rollingmean)
            listpos += 1
        elif (datapoint > rollingmean):
            window.append(datapoint)
            listpos += 1
        else:
            #maximum = max(window)
            beatposition = listpos - len(window) + (window.index(max(window)))
            peaklist.append(beatposition)
            window = []
            listpos += 1
    measures['peaklist'] = peaklist
    measures['ybeat'] = [dataset.RedSignal[x] for x in peaklist]
    measures['rolmean'] = rolmean
    calc_RR(dataset, samplingfreq)
    measures['rrsd'] = np.std(measures['RR_list'])
    
def fit_peaks(dataset, samplingfreq):
    ma_perc_list = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 150, 200, 300] #List with moving average raise percentages
    rrsd = []
    valid_ma = []
    for x in ma_perc_list: #Detect peaks with all percentages, append results to list 'rrsd'
        detect_peaks(dataset, x, samplingfreq)
        bpm = ((len(measures['peaklist'])/(len(dataset.RedSignal)/samplingfreq))*60)
        rrsd.append([measures['rrsd'], bpm, x])
        
    for x,y,z in rrsd: #Test list entries and select valid measures
        if ((x > 1) and ((y > 30) and (y < 130))):
            valid_ma.append([x, z])
            
    measures['best'] = min(valid_ma, key = lambda t: t[0])[1] #Save the ma_perc for plotting purposes later on (not needed)
    detect_peaks(dataset, min(valid_ma, key = lambda t: t[0])[1], samplingfreq) #Detect peaks with 'ma_perc' that goes with lowest rrsd
    
def calc_RR(dataset, samplingfreq):
    RR_list =[]
    peaklist = measures['peaklist']
    cnt = 0
    while (cnt < (len(peaklist) - 1)):
        RR_interval = (peaklist[cnt+1] - peaklist[cnt])
        ms_dist = ((RR_interval / samplingfreq) * 1000.0)
        RR_list.append(ms_dist)
        cnt += 1
    
    RR_diff = []
    RR_sqdiff = []

    count = 1 #use to iterate over RR/SS measures
    while (count < len(RR_list)-1):
        RR_diff.append(abs((RR_list[count] - RR_list[count+1]))) #calculate absolute difference between successive RR intervals
        RR_sqdiff.append(math.pow(RR_list[count] - RR_list[count+1], 2)) #calculate the squared difference
        count += 1
        
    measures['RR_list'] = RR_list
    measures['RR_diff'] = RR_diff
    measures['RR_sqdiff'] = RR_sqdiff
        
#function to calculate the time series HRV measures
def calc_ts_measures():
    RR_list = measures['RR_list']
    RR_diff = measures['RR_diff']
    RR_sqdiff = measures['RR_sqdiff']
    measures['bpm'] = 60000 / np.mean(RR_list)
    measures['ibi'] = np.mean(RR_list)
    measures['sdnn'] = np.std(RR_list)
    measures['sdsd'] = np.std(RR_diff)
    measures['rmssd'] = np.sqrt(np.mean(RR_sqdiff))
    nn20 = [x for x in RR_diff if (x > 20)]
    nn50 = [x for x in RR_diff if (x > 50)]
    measures['nn20'] = nn20
    measures['nn50'] = nn50
    measures['pnn20'] = float(len(nn20)) / float(len(RR_diff))
    measures['pnn50'] = float(len(nn50)) / float(len(RR_diff))
    
    
def plotter(dataset, title):
    peaklist = measures['peaklist']
    ybeat = measures['ybeat']
    plt.title(title)
    plt.ylim((16500, 20500))
    plt.plot(dataset.RedSignal, alpha=0.5, color='blue', label='raw signal')
    plt.plot(dataset.RedSignal_rollingmean, color='green', label='moving average')
    plt.scatter(peaklist, ybeat, color='red', label='average: %.1f BPM' %measures['bpm'])
    plt.legend(loc=4, framealpha=0.6)
    plt.show()

#finally we write a wrapper function to call the whole analysis quickly
def process(dataset, hrw, samplingfreq): #hrw is the 1-sided window size
    rolmean(dataset, hrw, samplingfreq)
    fit_peaks(dataset, samplingfreq)
    calc_RR(dataset, samplingfreq)
    calc_ts_measures()
    plotter(dataset, 'My Heartbeat Plot')
'''