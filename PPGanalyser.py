import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pandas as pd
import numpy as np
import math
from scipy import signal
from scipy.interpolate import UnivariateSpline

class PPGanalyser:
    def __init__(self, filename, column):
        self.filename = filename
        self.column = column
        self.measures = {}
    
    def load_data(self):
        self.data = pd.read_csv(self.filename)
        return self.data
    
    def remove_dc_offset(self, fc = 1.0, fs = 100.0):
        ''' Remove DC offset of the signal by 
        a high pass filter, the default cutoff 
        frequency (fc) is 1 Hz and 
        sampling frequency is 100 '''
        b, a = signal.butter(2, fc/(fs / 2.0), 'highpass')
        self.data[self.column] = signal.lfilter(b, a, self.data[self.column], 0)
        #self.data = self.data - mean(self.data)
        return self.data
    
    def calculate_rolling_mean(self, hrw, fs):
        mov_avg = pd.rolling_mean(self.data[self.column], window=int(hrw*fs)) #calculate the moving average
        avg_hr = (np.mean(self.data[self.column]))                            #impute where the moving average function returns
        mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
        mov_avg = [x*1.2 for x in mov_avg]
        self.data[self.column+'_'+'rollingmean'] = mov_avg
        return self.data
    
    def peak_detect(self, peak_threadhold):
        window = []
        peaklist = []
        ypeak = []
        listpos = 0
        for datapoint in self.data[self.column]:
            rollingmean = self.data[self.column+'_'+'rollingmean'][listpos]
            if (datapoint < rollingmean) and (len(window) < 1):
                listpos += 1
            elif datapoint > rollingmean:
                window.append(datapoint)
                listpos += 1
            else:
                maximum = max(window)
                beatposition = listpos - len(window) + (window.index(max(window)))
                if self.data[self.column][beatposition] > peak_threadhold:
                    peaklist.append(beatposition)
                    ypeak.append(self.data[self.column][beatposition])
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
        med_mad = np.median(self.measures['RR_list'])
        self.measures['hr_mad'] = np.median(np.abs(self.measures['RR_list'] - med_mad))
        return self.measures
    
    def calculate_f_domain(self, column, fs):
        RR_x = self.measures['peaklist'][1:]
        RR_y = self.measures['RR_list']
        RR_x_new = np.linspace(RR_x[0], RR_x[-1], RR_x[-1])
        interpolated_func = UnivariateSpline(rr_x, rr_y, k=5)
        datalen = len(self.)
        frq = np.fft.fftfreq(len(hrdata), d=((1/sample_rate)))
        frq = frq[range(int(datalen/2))]
        Y = np.fft.fft(interpolated_func(rr_x_new))/datalen
        Y = Y[range(int(datalen/2))]
        self.measures['lf'] = np.trapz(abs(Y[(frq >= 0.04) & (frq <= 0.15)]))
        self.measures['hf'] = np.trapz(abs(Y[(frq >= 0.16) & (frq <= 0.5)]))
        return self.measures['lf'], self.measures['hf']  
    


       

    