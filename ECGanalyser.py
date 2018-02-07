import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pandas as pd
import numpy as np
import math
from scipy import signal

class ECGanalyser:
    def __init__(self, filename):
        self.filename = filename
        self.measures = {}
    
    def load_data(self):
        self.data = pd.read_csv(self.filename)
        return self.data
    
    def remove_dc_offset(self, column, fc = 1.0, fs = 100.0):
        ''' Remove DC offset of the signal by 
        a high pass filter, the default cutoff 
        frequency (fc) is 1 Hz and 
        sampling frequency is 100 '''
        b, a = signal.butter(2, fc/(fs / 2.0), 'highpass')
        self.data[column] = signal.lfilter(b, a, self.data[column], 0)
        #self.data = self.data - mean(self.data)
        return self.data
    
    def calculate_rolling_mean(self, column, hrw, fs):
        mov_avg = pd.rolling_mean(self.data[column], window=int(hrw*fs)) #calculate the moving average
        avg_hr = (np.mean(self.data[column]))                            #impute where the moving average function returns
        mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
        mov_avg = [x*1.2 for x in mov_avg]
        self.data[column+'_'+'rollingmean'] = mov_avg
        return self.data
    
    def peak_detect(self, column, peak_threadhold):
        window = []
        peaklist = []
        ypeak = []
        listpos = 0
        for datapoint in self.data[column]:
            rollingmean = self.data[column+'_'+'rollingmean'][listpos]
            if (datapoint < rollingmean) and (len(window) < 1):
                listpos += 1
            elif datapoint > rollingmean:
                window.append(datapoint)
                listpos += 1
            else:
                maximum = max(window)
                beatposition = listpos - len(window) + (window.index(max(window)))
                if self.data[column][beatposition] > peak_threadhold:
                    peaklist.append(beatposition)
                    ypeak.append(self.data[column][beatposition])
                window = []
                listpos += 1
        self.measures['peaklist'] = peaklist
        self.measures['ybeat'] = ypeak
        return peaklist, ypeak
    
    def calculate_RR(self, fs):
        RR_list = []
        cnt = 0
        while (cnt < (len(self.measures['peaklist'])-1)):
            RR_interval = (self.measures['peaklist'][cnt+1] - self.measures['peaklist'][cnt])
            ms_dist = ((RR_interval / fs) * 1000.0)
            RR_list.append(ms_dist)
            cnt += 1
        self.measures['RR_list'] = RR_list
        
        RR_diff = []
        RR_sqdiff = []
        cnt = 0
        while (cnt < (len(RR_list)-1)):
            RR_diff.append(abs(RR_list[cnt] - RR_list[cnt+1]))
            RR_sqdiff.append(math.pow(RR_list[cnt] - RR_list[cnt+1], 2))
            cnt += 1
        self.measures['RR_diff'] = RR_diff
        self.measures['RR_sqdiff'] = RR_sqdiff
        return RR_list, RR_diff, RR_sqdiff
    
    def calculate_t_domain(self, fs):
        self.calculate_RR(fs)
        self.measures['bmp'] = round((60000 / np.mean(self.measures['RR_list'])))
        self.measures['ibi'] = np.mean(self.measures['RR_list'])
        self.measures['sdnn'] = np.std(self.measures['RR_list'])
        self.measures['sdsd'] = np.mean(self.measures['RR_diff'])
        self.measures['rmssd'] = np.sqrt(np.mean(self.measures['RR_sqdiff']))
        NN20 = [x for x in self.measures['RR_diff'] if (x>20)]
        NN50 = [x for x in self.measures['RR_diff'] if (x>50)]
        self.measures['nn20'] = NN20
        self.measures['nn50'] = NN50
        self.measures['pnn20'] = float(len(NN20)) / float(len(self.measures['RR_diff']))
        self.measures['pnn50'] = float(len(NN50)) / float(len(self.measures['RR_diff']))
        return bpm
    
def calc_ts_measures():
    RR_list = measures['RR_list']
    RR_diff = measures['RR_diff']
    RR_sqdiff = measures['RR_sqdiff']
    measures['bpm'] = 60000 / np.mean(RR_list)
    measures['ibi'] = np.mean(RR_list)
    measures['sdnn'] = np.std(RR_list)
    measures['sdsd'] = np.std(RR_diff)
    measures['rmssd'] = np.sqrt(np.mean(RR_sqdiff))
    NN20 = [x for x in RR_diff if (x>20)]
    NN50 = [x for x in RR_diff if (x>50)]
    measures['nn20'] = NN20
    measures['nn50'] = NN50
    measures['pnn20'] = float(len(NN20)) / float(len(RR_diff))
    measures['pnn50'] = float(len(NN50)) / float(len(RR_diff))

       

    