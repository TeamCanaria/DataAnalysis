#Library for Hilbert
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert, kaiserord, convolve, firwin, freqz #get_window, kaiser
#import matplotlib.pylab as plt

def bandpassKaiser(dat, fs, pass1, pass2, viewfilter):
    n, beta = kaiserord(401, 0.1)

    wind = firwin((n + np.remainder(n,2))+1, [pass1,pass2], window=('kaiser', beta), pass_zero=False, nyq = 180)#fs*2)   
    
    if (viewfilter == 1):
        w, h = freqz(wind)
        plt.figure(2)
        plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
        plt.xlim(0, 0.5*fs)
        plt.title("BandPass Filter Frequency Response")
        plt.xlabel('Frequency [Hz]')
        plt.grid()  
    
    wind = np.reshape(wind, [len(wind), 1]) 
    
    flt = convolve(dat, wind, mode='full')
    
    s = len(flt)

    filtered_dat = flt[(int(n/2)+1):(s-int(n/2)-1)]
    
    return (filtered_dat)

def VariableThresh(data, SBL, TD, meth):        #SBL = search back length for the moving threshold ; TD = threshold difficulty factor (ratio of height between mean and max) ; meth = 1 for mean, meth = 2 for STD
    LD = len(data)                              #Data = data moving threshold is applied upon - different for different applications (e.g. plain data, filtered data or post HT data)
    thresh = np.zeros(LD)                       #Set TD between 1 & 2
    
    for i in range(SBL):
        thresh[i] = np.mean(data[0:SBL-1]) + 0.8*np.std(data[0:SBL-1])

    if (meth == 1):
        TD = TD - 1
        no_max = 5                                  #How many points to try and pull mean up by
        temp_max = np.zeros(no_max)
        fac = int(SBL/5)
            
        for i in range(SBL, LD):
            for j in range(1,no_max):
                temp_max[j] = np.max(data[(i-(fac*j)):(i-fac*(j-1))])
            
            thresh[i] = TD*(np.mean(temp_max) - np.mean(data[(i-SBL):i])) + np.mean(data[(i-SBL):i])
    
    if (meth == 2):
        for i in range(SBL, LD):        
            thresh[i] = TD*(np.std(data[(i-SBL):i])) + np.mean(data[(i-SBL):i])
    
    if (meth == 3):
        for i in range(SBL,LD,SBL):
            thresh[i-SBL:i] = TD*(np.std(data[(i-SBL):i])) + np.mean(data[(i-SBL):i])
            
        if i < LD:
            thresh[i:LD] = TD*(np.std(data[i:LD])) + np.mean(data[i:LD])
        
    return(thresh)

def edges(x, thresh):
    
    N = len(x)
    poss_reg = np.empty((N,1), dtype=bool)
    
    for i in range(N):
        poss_reg[i] = x[i] > thresh[i]    
   
    NN = poss_reg.size
    Hold = np.zeros(NN)
    Left = np.zeros(NN)
    Right = np.zeros(NN)
        
    for i in range(1,NN):
        if ((poss_reg[i] ^ poss_reg[i-1]) == 1):
            Hold[i] = i-1
    
    Hold = Hold[Hold!=0]   
    M = Hold.size
    MM = np.int(M/2)
    
    if (poss_reg[0] == False):
        Left[0] = Hold[0]
        Right[0] = Hold[1]
        flag = 0
    else: 
        Right[0] = Hold[0]
        Left[0] = 1
        flag = 1
    
    if (flag == 1):
        for i in range(1, MM):
            Right[i] = Hold[i*2]
            Left[i] = Hold[i*2-1]+1
        Right[MM] = NN
    else:
        for i in range(0, MM):
            Left[i] = Hold[i*2]+1
            Right[i] = Hold[i*2+1]       
    
    Right = Right[Right!=0]
    Left = Left[Left!=0]  
    
    return(Left, Right)   

# =============================================================================
# def edges(x, thresh):
#     
#     N = len(x)
#     poss_reg = np.empty((N,1), dtype=bool)
#     
#     for i in range(N):
#         poss_reg[i] = x[i] > thresh[i]    
#     
#     NN = poss_reg.size
#     Hold = np.zeros(NN)
#     Left = np.zeros(NN)
#     Right = np.zeros(NN)
#         
#     for i in range(1,NN):
#         if ((poss_reg[i] ^ poss_reg[i-1]) == 1):
#             Hold[i] = i
#     
#     Hold = Hold[Hold!=0]   
#     M = Hold.size
#     MM = np.int(M/2)
#     
#     if (poss_reg[0] == False):
#         Left[0] = Hold[0]
#         Right[0] = Hold[1]
#         flag = 0
#     else: 
#         Right[0] = Hold[0]
#         Left[0] = 1
#         flag = 1
#     
#     if (flag == 1):
#         for i in range(1, MM):
#             Right[i] = Hold[i*2]
#             Left[i] = Hold[i*2-1]
#         
#     else:
#         for i in range(0, MM):
#             Left[i] = Hold[i*2]
#             Right[i] = Hold[i*2+1]       
#     
#     if (np.remainder(M,2) == 0):  
#         Right[MM] = NN
#         Left[MM] = Hold[M-1]
#     else:
#         Right[MM] = Hold[M-1]
#     
#     Right = Right[Right!=0]
#     Left = Left[Left!=0]  
# 
#     return(Left, Right)                     
# =============================================================================

def edges2(x):
    
    N = len(x)

    poss_reg = np.empty((N,1), dtype=bool)

    poss_reg = x > 0   
    
    NN = poss_reg.size
    Hold = np.zeros(NN)
    Left = np.zeros(NN)
    Right = np.zeros(NN)
        
    for i in range(1,NN):
        if ((poss_reg[i] ^ poss_reg[i-1]) == 1):
            Hold[i] = i
    
    Hold = Hold[Hold!=0]   
    M = Hold.size
    MM = np.int(M/2)
    
    if (poss_reg[0] == False):
        Left[0] = Hold[0]
        Right[0] = Hold[1]
        flag = 0
    else: 
        Right[0] = Hold[0]
        Left[0] = 1
        flag = 1
    
    if (flag == 1):
        for i in range(1, MM):
            Right[i] = Hold[i*2]
            Left[i] = Hold[i*2-1]
        
    else:
        for i in range(0, MM):
            Left[i] = Hold[i*2]
            Right[i] = Hold[i*2+1]       
    
    if (np.remainder(M,2) == 0):  
        Right[MM] = NN
        Left[MM] = Hold[M-1]
    else:
        Right[MM] = Hold[M-1]
    
    Right = Right[Right!=0]
    Left = Left[Left!=0]  
    
    return(Left, Right)        


def HillTransform(fs, raw, k_filt):
    k_filt = k_filt[:]
    N = raw.size

    if (len(k_filt) != 1):
        s = np.transpose(k_filt)
    else:
        s = k_filt
                             
    s2 = np.abs(hilbert(s))
    xe = np.abs(s2) # + np.abs(s)
    
    h = np.true_divide(np.ones((1,31)), 31)
    Delay = 15
    
    x = np.convolve(np.ravel(xe), np.ravel(h)) 
    x = x[np.arange(Delay, N)]
    x = np.true_divide(x, np.max(np.abs(x)))
    
    return (x)

def PeakSearch(data, raw, thr, pol):

    min_L = 10                                      # sets minimum amount of values which must be above threshold

    (left, right) = edges(data, thr)                    
    NN = left.size
    R_loc = np.zeros(NN)
    if (pol == 1):

        
        for i in range(NN):
            z = np.arange(int(left[i]), int(right[i])+1)
            if (np.size(z) > min_L):
                temp1 = np.max(raw[z])
                temp2 = np.argmax(raw[(z)])
                temp3 = np.min(raw[z])
                temp4 = np.argmin(raw[(z)])
                
                if (np.abs(temp1-raw[int(left[i])]) > np.abs(temp3-raw[int(left[i])])):
                      R_loc[i] = temp2
                else:
                      R_loc[i] = temp4
            
                R_loc[i] = R_loc[i] + left[i]            
        
        R_loc = R_loc[R_loc!=0]
    else:
        for i in range(NN):
            z = np.arange(int(left[i]), int(right[i])+1)
            R_loc[i] = np.argmax(data[(z)])
            R_loc[i] = R_loc[i] + left[i]  

    return(R_loc)                 

def Correction_Al(peaks, fs, raw):
    min_L = 60/200*fs

    M = peaks.size

    for i in range(1, M):
        if (peaks[i]-peaks[i-1] <= min_L):
            temp1 = np.abs(raw[int(peaks[i])])
            temp2 = np.abs(raw[int(peaks[i-1])])
            if (temp2 > (temp1+0.1*temp1)) | (temp2 < (temp1-0.1*temp1)):
                slope1 = (0.5*(raw[int(peaks[i-1])] - raw[int(peaks[i-1])-1]) + 0.5*(raw[int(peaks[i-1])-1] - raw[int(peaks[i-1])-2]))/(1/fs)
                slope2 = (0.5*(raw[int(peaks[i])] - raw[int(peaks[i])-1]) + 0.5*(raw[int(peaks[i])-1] - raw[int(peaks[i])-2]))/(1/fs)
                
                if (np.abs(slope2)>np.abs(slope1)):
                    peaks[i-1] = 0
                else:
                    peaks[i]=0
    
   
    peaks = peaks[peaks!=0]

    return (peaks)

def PeakSearch2(data, raw, thr):

    min_L = 10                                      # sets minimum amount of values which must be above threshold
    min_LL = 120                                    # Helps identify T-waves
    min_LLL = 0.2

    (left, right) = edges(data, thr)                    
    
    NN = left.size

    R_value = np.zeros(NN)
    R_loc = np.zeros(NN)
    for i in range(NN):
        z = np.arange(int(left[i]), int(right[i]))

        if (np.size(z) > min_L):
            temp1 = np.max(raw[(z)])
            temp2 = np.argmax(raw[(z)])
            temp3 = np.min(raw[(z)])
            temp4 = np.argmin(raw[(z)])       

            if (np.abs(temp1-raw[int(left[i])]) > np.abs(temp3-raw[int(left[i])])):
                 R_value[i] = temp1
                 R_loc[i] = temp2
            else: 
                 R_value[i] = temp3
                 R_loc[i] = temp4

            R_loc[i] = temp2         
            R_loc[i] = R_loc[i] + left[i]             
    

    for q in range(np.size(R_loc)):
        if (R_loc[q] == 0):
             R_value[q] = 0
     
    R_loc = R_loc[R_loc!=0]
    R_value = R_value[R_value!=0]
     
    M = R_loc.size
    N = R_value.size
    print(M) 
    print(N)
     
    for i in range(1, M):
        if (R_loc[i]-R_loc[i-1] < min_LL):
            if ((np.abs(R_value[i] - R_value[i-1])) < min_LLL):                 #Check to see if both identified points are R-peaks
                if (np.abs(R_value[i]) > np.abs(R_value[i-1])):                                 #Eliminates smaller amplitude value as the assumed T-wave
                    R_loc[i-1] = 0
                else:
                    R_loc[i] = 0
     
    R_loc = R_loc[R_loc!=0]
 

    return(R_loc)                          

def T_search(dat, R):
    N = len(R)
    T_peaks = np.zeros(N)
    T_peak_amp = np.zeros(N)
    
    for i in range(N-1):
        if ((R[i+1]-R[i]) > 150) :
            space = dat[(int(R[i])+50):(int(R[i+1])-100)]
            T_peaks[i] = np.argmax(space)+(int(R[i])+50)
            T_peak_amp[i] = np.max(space)
    
    space = dat[(int(R[N-1])):(len(dat)-1)]
    
    if (len(space) > 50):
        T_peaks[N-1] = np.argmax(space)
        T_peak_amp[N-1] = np.max(space)   
    else:
        T_peaks = T_peaks[0:N-1]
        T_peak_amp = T_peak_amp[0:N-1]
    
    return(T_peaks, T_peak_amp)


def S_search(dat, R, T, ddt):
    
    N = len(T)
    S_peaks = np.zeros(N)
    
    for i in range(N):
        space = dat[int(R[i]):int(T[i])]
        
        if (len(space) > 0):
            temp = np.argmin(space)
            
            if (space[temp+3] > space[temp+2] > space[temp+1] > space[temp]):
                S_peaks[i] = temp + int(R[i])
                       
            else:
                space = ddt[int(R[i]):int(T[i])]
                (Left, Right) = edges2(ddt[int(R[i]):int(T[i])])
                
                for j in range(len(Left)):
                    if ((Right[j]-Left[j]) > 3):
                        S_peaks[i] = Left[j] + int(R[i]) - 1
                        break;
                    #S_peak_amp = dat[int(S_peaks[i])]
    
    S_peaks = S_peaks[S_peaks!=0]
    
    return(S_peaks)#, S_peak_amp)