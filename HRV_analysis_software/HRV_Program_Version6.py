from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
import tkinter as tk
import h5py
import numpy as np
import tkinter.constants as TKc
import sys
import os
from Hill_lib2 import bandpassKaiser, HillTransform, PeakSearch, VariableThresh
from ECG_Processing_main import ECG_processing

#from Mains_lib import acc, test

# ~~~~~~~~~~~~~~ GLOBAL VARIABLES ~~~~~~~~~~~~~~~~~~~#
global xmaxx
global xminn
global ymaxx
global yminn
global yrange
global xxrange
global westerly
global easterly
global ts
global trpd
global cnt 
global bound1   
global invert_flag
global labelled_flag
global ent1
global ent2
global cid
global cid1
global dat
global R_t
global R_amp  
global val
global x

global root
global frame
global mmwin
global colwin
global paitentfile
global window 
global scroll
global graphCanvas
global xx
global frame2
global window2
global RR_interval_Canvas
global xx2
global w 
global h
global placeholder
global entry1
global entry2
global b5



global ent11
global ent22
global ent33
global ent44
global predict_flag
global Fs
global column_number
global column_number2
column_number = 1
column_number2 = 1
#Fs = 360
predict_flag = 0
bound1 = 20
invert_flag = 0

easterly = 10000
westerly = 1050
ts = 0
trpd = 45

XX = 16200
YY = 1000
yplott = np.zeros(XX)
# ~~~~~~~~~~~~~~ WINDOW CONTROL FUNCTIONS ~~~~~~~~~~~~~~~~~~~#3
def exiter():
    mmwin.withdraw()
    sys.exit() 

def exiter2():
    colwin.withdraw()
    sys.exit()     

def exiter3():
    mm2win.withdraw()
    sys.exit() 

def exiter4():
    col2win.withdraw()
    sys.exit()
    
def GetFile():
    global paitentfile
    global mmwin
    paitentfile = tk.filedialog.askopenfilename ()
    label11=tk.Label(mmwin, text=paitentfile, bg="white", anchor = TKc.W, width = 40)
    label11.grid(row=0,column=1) 

def GetFile2():
    global annfile
    global mm2win
    annfile = tk.filedialog.askopenfilename ()
    label11=tk.Label(mm2win, text=annfile, bg="white", anchor = TKc.W, width = 40)
    label11.grid(row=0,column=1) 

def modemenu():
    global mmwin
    global paitentfile
    mmwin = tk.Tk()
    mmwin.title('Choose Patient File')
    mmwin.bind('<Escape>', exiter)
    paitentfile = "Choose a patient file ..."
    mmwinfr1 = tk.Frame(mmwin, height="150", width="300")
    mmwinfr1.grid(row=0,column=0, rowspan=2, columnspan=3, sticky=TKc.W+TKc.E+TKc.N+TKc.S)
    label1=tk.Label(mmwinfr1, text="Data Base :", bg="white", anchor = TKc.W, width = 20)
    label1.grid(row=0,column=0)
    label1=tk.Label(mmwinfr1, text=paitentfile, bg="white", anchor = TKc.W, width = 40)
    label1.grid(row=0,column=1)    
    butn0 = tk.Button(mmwinfr1, text="Browse", width=10, command=GetFile)
    butn0.grid(row=0, column=2)
    
    mmwinfr2 = tk.Frame(mmwin, height="300", width="200", bg="green")
    mmwinfr2.grid(row=2,column=0, rowspan=2, columnspan=3, sticky=TKc.W+TKc.E+TKc.N+TKc.S)
    butn1 = tk.Button(mmwinfr2, text="Launch", width=10, command=Launcher)
    butn1.grid(row=0, column=0)    
    butn2 = tk.Button(mmwinfr2, text="Quit", width=20, command=exiter)
    butn2.grid(row=0, column=3, sticky=TKc.E)   
 
    mmwin.mainloop()
    
def modemenu2():
    global mm2win
    global annfile
    
    mm2win = tk.Tk()
    mm2win.title('Choose Annotation File')
    mm2win.bind('<Escape>', exiter3)
    annfile = "Choose an annotation file ..."
    mm2winfr1 = tk.Frame(mm2win, height="150", width="300")
    mm2winfr1.grid(row=0,column=0, rowspan=2, columnspan=3, sticky=TKc.W+TKc.E+TKc.N+TKc.S)
    label1=tk.Label(mm2winfr1, text="Data Base :", bg="white", anchor = TKc.W, width = 20)
    label1.grid(row=0,column=0)
    label1=tk.Label(mm2winfr1, text=annfile, bg="white", anchor = TKc.W, width = 40)
    label1.grid(row=0,column=1)    
    butn0 = tk.Button(mm2winfr1, text="Browse", width=10, command=GetFile2)
    butn0.grid(row=0, column=2)
    
    mm2winfr2 = tk.Frame(mm2win, height="300", width="200", bg="blue")
    mm2winfr2.grid(row=2,column=0, rowspan=2, columnspan=3, sticky=TKc.W+TKc.E+TKc.N+TKc.S)
    butn1 = tk.Button(mm2winfr2, text="Launch", width=10, command=Launcher2)
    butn1.grid(row=0, column=0)    
    butn2 = tk.Button(mm2winfr2, text="Quit", width=20, command=exiter3)
    butn2.grid(row=0, column=3, sticky=TKc.E)   
 
    mm2win.mainloop()    

def column_selector():
    global Fs
    global butt1
    global butt2
    global butt3
    global colwin
    global frq_ent
    colwin = tk.Tk()
    colwin.title('Sampling Frequency and Column/Row Selection')
    colwin.bind('<Escape>', exiter2)    
    label1=tk.Label(colwin, text="Sampling Frequency :", bg="white", anchor = TKc.W, width = 30)
    label1.grid(row=0,column=0)   
    frq_ent=tk.Entry(colwin, width = 20)
    frq_ent.grid(row=0,column=1,columnspan=3)
    
    
    label2=tk.Label(colwin, text="Column/Row of ECG signal:", bg="white", anchor = TKc.W, width = 30)
    label2.grid(row=1,column=0) 
    

    butt1 = tk.Button(colwin, text=1, width=5,command = lambda:data_col(1), relief = "raised")
    butt1.grid(row=1, column=1)
    butt2 = tk.Button(colwin, text=2, width=5,command = lambda:data_col(2), relief = "raised")
    butt2.grid(row=1, column=2)
    butt3 = tk.Button(colwin, text=3, width=5,command = lambda:data_col(3), relief = "raised")
    butt3.grid(row=1, column=3)
    
    buttn1 = tk.Button(colwin, text="Ok", width=10, command=int_settings)
    buttn1.grid(row=2, column=0)    
    buttn2 = tk.Button(colwin, text="Quit", width=20, command=exiter2)
    buttn2.grid(row=2, column=1,columnspan=3)   

def column_selector2():
    global root
    global R_t
    global R_amp
    global labelled_flag
    
    R_t = []
    R_amp = []
    labelled_flag = 0
    
    root.withdraw()
    column_selector()

def column_selector3():
    global Fs
    global butt11
    global butt12
    global butt13
    global col2win
    
    col2win = tk.Tk()
    col2win.title('Column/Row Selection')
    col2win.bind('<Escape>', exiter2)        
    
    label2=tk.Label(colwin, text="Column/Row of ECG signal:", bg="white", anchor = TKc.W, width = 30)
    label2.grid(row=0,column=0) 
    

    butt11 = tk.Button(col2win, text=1, width=5,command = lambda:data_col2(1), relief = "raised")
    butt11.grid(row=0, column=1)
    butt12 = tk.Button(col2win, text=2, width=5,command = lambda:data_col2(2), relief = "raised")
    butt12.grid(row=0, column=2)
    butt13 = tk.Button(col2win, text=3, width=5,command = lambda:data_col2(3), relief = "raised")
    butt13.grid(row=0, column=3)
    
    buttn11 = tk.Button(col2win, text="Ok", width=10, command=ann_int)
    buttn11.grid(row=1, column=0)    
    buttn12 = tk.Button(col2win, text="Quit", width=20, command=exiter4)
    buttn12.grid(row=1, column=1,columnspan=3)  
    
def data_col(clm):
    global column_number
    global butt1
    global butt2
    global butt3   
    
    if clm == 1:
        butt1.config(relief="sunken")
        butt2.config(relief="raised")
        butt3.config(relief="raised")
    elif clm == 2:
        butt1.config(relief="raised")
        butt2.config(relief="sunken")
        butt3.config(relief="raised")
    else:
        butt1.config(relief="raised")
        butt2.config(relief="raised")
        butt3.config(relief="sunken")        
        
    column_number = clm

def data_col2(clm):
    global column_number2
    global butt11
    global butt12
    global butt13   
    
    if clm == 1:
        butt11.config(relief="sunken")
        butt12.config(relief="raised")
        butt13.config(relief="raised")
    elif clm == 2:
        butt11.config(relief="raised")
        butt12.config(relief="sunken")
        butt13.config(relief="raised")
    else:
        butt11.config(relief="raised")
        butt12.config(relief="raised")
        butt13.config(relief="sunken")        
        
    column_number2 = clm

def ann_int():
    global col2win
    global column_number2
    global og_ann
    global R_t
    global R_amp
    global dat
    
    R_t = []

    R_t = og_ann[:,(column_number-1)]
    R_t = np.reshape(R_t, [len(R_t),1])
    
    R_amp = np.zeros(np.size(R_t))
    for i in range(0, np.size(R_t)):
        R_amp[i]= dat[int(R_t[i]) - 1]
    
    col2win.withdraw()
    draw() 


def Launcher2(): 
    global mm2win
    global annfile
    global og_ann
    global va
    global x
    global labelled_flag

    filename, file_extension = os.path.splitext(annfile)

    if file_extension == '.txt':
        file = open(annfile, 'r')
        
        temp = file.read().split()
        var1 = len(temp)
        
        og_ann = np.zeros(np.size(temp))
        for i in range(len(temp)):
            og_ann[i] = float(temp[i].rstrip('\n'))
        
        file.seek(0)
        temp2 = file.readlines()
        
        var2 = len(temp2)
        
        columns = var1/var2
        
        og_ann = np.reshape(og_ann, [len(temp2), int(columns)])
        
        if (columns > var2):
            og_ann = np.transpose(og_ann)
        
        file.close()
        labelled_flag = 1
             
     #   sys.exit()
        mm2win.withdraw()
        column_selector3()
#HERRHERHERH RHE RR A NAKE OEHGBH GBH RTHGFD BBUL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # #         
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
    elif file_extension == '.h5':
        fol_name = annfile
        file = h5py.File(fol_name, 'r')    
    
        h5popup(2)
    

def Get_ent(type__):
    global f_name
    global fileh5
    global h5pu
    f_name = str(fileh5.get())

    if (len(f_name) > 0):
        h5pu.withdraw()
        Launcher_part_2(type__)

def h5popup(type_):
    global fileh5
    global h5pu
    
    h5pu = tk.Tk()
    h5pu.title('h5 Subfolder selection')      
    
    lab=tk.Label(h5pu, text="Please enter the desired file extension: ", bg="white", anchor = TKc.W, width = 30)
    lab.grid(row=0,column=0) 

    fileh5=tk.Entry(h5pu, width=30)
    fileh5.grid(row=0,column=1)
    
    if type_ == 1:
        but=tk.Button(h5pu, text="Ok", width=10, command = lambda: Get_ent(1))
        but.grid(row=0,column=2)
    else:
        but=tk.Button(h5pu, text="Ok", width=10, command = lambda: Get_ent(2))
        but.grid(row=0,column=2)
    h5pu.mainloop()
    
    
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # # #  
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
def Launcher(): 
    global mmwin
    global paitentfile
    global og_dat
    global R_t
    global R_amp  
    global x
    global labelled_flag
    global file

    filename, file_extension = os.path.splitext(paitentfile)

    if file_extension == '.txt':
        file = open(paitentfile, 'r')
        
        if len(paitentfile) == 0:
            print('Error with file')
        
        else:        
            print('File opened successfully: ' , paitentfile)
        
        temp = file.read().split()
        var1 = len(temp)
        
        og_dat = np.zeros(np.size(temp))
        for i in range(len(temp)):
            og_dat[i] = float(temp[i].rstrip('\n'))
        
        file.seek(0)
        temp2 = file.readlines()
        
        var2 = len(temp2)
        
        columns = var1/var2
        
        og_dat = np.reshape(og_dat, [len(temp2), int(columns)])
        
        if (columns > var2):
            og_dat = np.transpose(og_dat)
        
        file.close()
    
        R_t = []
        R_amp = []
             
        
        if (len(R_t) == 0):
            labelled_flag = 0
        else: 
            labelled_flag = 1
             
     #   sys.exit()
        mmwin.withdraw()
        column_selector()
        
    elif file_extension == '.h5':        
        fol_name = paitentfile
        file = h5py.File(fol_name, 'r')    
        h5popup(1)
    
def Launcher_part_2(type_):
    global file
    global f_name
    global og_dat
    global R_t
    global R_amp  
    global labelled_flag
    global og_ann
    
    if type_ == 1:
        og_dat = file[f_name] 
        og_dat = og_dat[:]
    
        row, col = np.shape(og_dat)
        if (col > row):
            og_dat = np.transpose(og_dat)    
            
        R_t = []
        R_amp = []
        
        labelled_flag = 0
    
        mmwin.withdraw()
        column_selector()
        
    else:
        og_ann = file[f_name] 
        og_ann = og_ann[:]

        row, col = np.shape(og_dat)
        if (col > row):
            og_ann = np.transpose(og_ann)    

        labelled_flag = 1

        mm2win.withdraw()
        column_selector3()
        # =============================================================================
#     
# import scipy.io as sio
# 
# file_name = input('Input matlab filename to open: ')
# 
# open_file = sio.loadmat(file_name)
# 
# if len(file_name) == 0:
#     print('Error because no file name was inputted')
#     
# else:
#     print('File opened successfully: ' , file_name)    
# =============================================================================

def save_window():
    global ent1
    global ent2
    global swin
    global save_but1
    global save_but2

    swin = tk.Tk()
    swin.title('Save Window')
    
    
    lab1=tk.Label(swin, text="Folder Location", anchor = TKc.W, width = 20)
    lab1.grid(row=1,column=0)
    ent1 = tk.Entry(swin)
    ent1.grid(row=1,column=1)
    
    lab2=tk.Label(swin, text="Patient", anchor = TKc.W, width = 20)
    lab2.grid(row=2,column=0)
    ent2 = tk.Entry(swin)
    ent2.grid(row=2, column=1)


    butt = tk.Button(swin, text="Save", width=10, command=Export_data)
    butt.grid(row=4,column=0) #sticky=TKc.S
    
    opps = tk.Button(swin, text="Cancel", width=10, command=exitsave)
    opps.grid(row=4, column=1)
    
    save_but1 = tk.Button(swin, text="Existing", width=10, command= lambda: read_write_save_toggle(1), relief="raised")
    save_but1.grid(row=0,column=0)
   
    save_but2 = tk.Button(swin, text="New", width = 10, command = lambda: read_write_save_toggle(0), relief="raised")
    save_but2.grid(row=0, column=1)
    
def read_write_save_toggle(flag):
    global swin
    global save_but1
    global save_but2
    global savetype
    
    savetype = flag
    
    if flag == 1:
        save_but1.config(relief="sunken")
        save_but2.config(relief="raised")
    else:
        save_but1.config(relief = "raised")
        save_but2.config(relief = "sunken")
            
def Export_data():
    global ent1
    global ent2  
    global savetype
    
    folder_loc_temp = str(ent1.get())   
    val = str(ent2.get())
    
    if len(folder_loc_temp) == 0:
        f_name = '/home/meghan/Desktop/Python/Random.h5'
        
    else:
        f_name = folder_loc_temp
        
    if savetype == 1:
        f = h5py.File(f_name, 'r+')
    else:
        f = h5py.File(f_name, 'w')

    name1 = '//' + str(val) + '/amp'
    name2 = '//' + str(val) + '/time'
                         
    f.create_dataset(name1, data = R_amp)    
    f.create_dataset(name2, data = R_t)

    swin.withdraw()

def Prediction_mode(mode_type):
    global dat    
    global R_t
    global R_amp
    global b6
    global xminn
    global xmaxx
    global labelled_flag
    
    if b6.config('relief')[-1] == 'raised':
        if mode_type == 1:
            #========================== Set Values =========================#
            labelled_flag = 1
            fs = Fs
            viewfilter = 0
            highpass_cut = 5
            lowpass_cut = 40
            #dat = dat[xminn:xmaxx]
        
            #====================== Conduct Predictions =======================#
            flt_dat = bandpassKaiser(dat, fs, highpass_cut, lowpass_cut, viewfilter)
            flt_dat = flt_dat[:] 
            
            x = HillTransform(fs, dat, flt_dat)             # X = derivative
            thr = VariableThresh(x, 2000, 1.25, 1)
            predictions = PeakSearch(x, dat, thr, 1)          ################made changes on this line for thresh    
        
            R_t = predictions        
            siz = np.size(R_t)
            R_t = np.reshape(R_t, [siz,1])
            
            R_amp = np.zeros(siz)
            for i in range(siz):
                R_amp[i] = dat[int(R_t[i])]  
        
            if (len(R_amp) == 1):
                R_amp = np.transpose(R_amp)
            
            b6.config(text = "Cancel Prediction Mode", relief = "sunken")
            
            draw()
        elif mode_type == 3:
            #========================== Set Values =========================#
            labelled_flag = 1
            fs = Fs
            viewfilter = 0
            highpass_cut = 5
            lowpass_cut = 40
            #dat = dat[xminn:xmaxx]
        
            #====================== Conduct Predictions =======================#
            flt_dat = bandpassKaiser(dat, fs, highpass_cut, lowpass_cut, viewfilter)
            flt_dat = flt_dat[:]

            R_t = ECG_processing(dat)
            siz = np.size(R_t)
            R_t = np.reshape(R_t, [siz,1])
            
            R_amp = np.zeros(siz)
            for i in range(siz):
                R_amp[i] = dat[int(R_t[i])]  
        
            if (len(R_amp) == 1):
                R_amp = np.transpose(R_amp)
            
            b6.config(text = "Cancel Prediction Mode", relief = "sunken")
            
            draw()            
        else:
            print('not imported yet')
    else:
        R_t = []
        R_amp = []
        labelled_flag = 0
        b6.config(text = "Launch Prediction Mode", relief="raised")
        draw()
        
# ~~~~~~~~~~~~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~#
def Jump():
    global xmaxx
    global xminn
    global ymaxx
    global yminn
    global yrange
    global xxrange
    global ts
    global trpd
    global R_t
    global R_amp
    global dat
    
    temp1 = entry1.get()
    temp2 = entry2.get()
   
    if len(temp1) > 0:
        ts = int(temp1)

    if len(temp2) > 0:
        trpd = int(temp2)

    xminn = (ts*Fs)
    xmaxx = xminn+(trpd*Fs)
    ymaxx = np.max(dat[xminn:xmaxx])+0.1
    yminn = np.min(dat[xminn:xmaxx])-0.1
    yrange = ymaxx-yminn
    xxrange = xmaxx-xminn
    
    draw()
    
def Jump2(val):
    global xmaxx
    global xminn
    global ymaxx
    global yminn
    global xxrange
    global ts    
    global trpd
    global R_t
    global R_amp
    global dat
    
    
    ts=int(val)

    trpd = xxrange/Fs

    xminn = ts*Fs
    xmaxx = xminn+xxrange
    ymaxx = np.max(dat[xminn:xmaxx])+0.1
    yminn = np.min(dat[xminn:xmaxx])-0.1

                  
                  
    draw()

def AdjustDisplay(val):
    global xmaxx
    global xminn
    global ymaxx
    global yminn
    global xxrange
    global ts
    global trpd
    global R_t
    global R_amp
    global dat
    
    ts = xminn/Fs
    trpd = val
    
    xmaxx = xminn + val*Fs
    ymaxx = np.max(dat[xminn:xmaxx])+0.1
    yminn = np.min(dat[xminn:xmaxx])-0.1
    xxrange = xmaxx - xminn
                  
    draw()


def ShiftLeft():
    global xmaxx
    global xminn
    global ymaxx
    global yminn
    global yrange
    global xxrange
    global ts
    global trpd
    global R_t
    global R_amp
    global dat
    
    shift = trpd*Fs
    
    if (xminn > shift):
        xminn = xminn - trpd*Fs   
        xmaxx = xmaxx - trpd*Fs
        ymaxx = np.max(dat[xminn:xmaxx])+0.1
        yminn = np.min(dat[xminn:xmaxx])-0.1
    
        
    else:
        xminn = 0
        xmaxx = xxrange
        ymaxx = np.max(dat[xminn:xmaxx])+0.1
        yminn = np.min(dat[xminn:xmaxx])-0.1
        
    
    ts = xminn/Fs
                
    draw()   
       
def ShiftRight():
    global xmaxx
    global xminn
    global ymaxx
    global yminn
    global yrange
    global xxrange
    global trpd
    global ts
    global R_t
    global R_amp
    global dat
    
    shift = trpd*Fs
    
    if (xmaxx < (650000 - shift)):
        xminn = xminn + trpd*Fs  
        xmaxx = xmaxx + trpd*Fs
        ymaxx = np.max(dat[xminn:xmaxx])+0.1
        yminn = np.min(dat[xminn:xmaxx])-0.1 
        
        
    else:
        xmaxx = 654999
        xminn = xmaxx-xxrange
        ymaxx = np.max(dat[xminn:xmaxx])+0.1
        yminn = np.min(dat[xminn:xmaxx])-0.1  
                      
    ts = xminn/Fs
    draw()
    
def Move():
    global xmaxx
    global xminn
    global ymaxx
    global yminn
    global yrange
    global xxrange
    global easterly
    global westerly
    global R_t
    global R_amp
    global dat
    global predict
    global amp

    (xminn, xmaxx) = scroll.get()
    ymaxx = np.max(dat[xminn:xmaxx])+0.1
    yminn = np.min(dat[xminn:xmaxx])-0.1
    yrange = ymaxx-yminn
    xxrange = xmaxx-xminn
    easterly = xminn
    westerly = xmaxx
    
    draw()

def draw():
    global x
    global xxmin
    global xxmax
    global yminn
    global ymaxx
    global R_t
    global R_amp
    global labelled_flag
    global dat
    global plot_fig
    global graphCanvas
    global fig
    global left
    global right

    x_plot = x[xminn:xmaxx]
    plot_dat = dat[xminn:xmaxx]
        
    #Top Figure
    plot_fig.clear()
    plot_fig.plot(x_plot/Fs, plot_dat, color ='r', linewidth=1)
    
    if (labelled_flag == 1): 
        plot_fig.plot(R_t/Fs, R_amp, 'bo', linewidth = 1) 
    plot_fig.axis([xminn/Fs,xmaxx/Fs,yminn,ymaxx])#([xminn,xmaxx,yminn,ymaxx])
    graphCanvas.show()
    
    draw2()
    
def draw2(): 
    global ts
    global trpd
    global R_t
    global R_amp
    global dat
    global x
    global fig2
    global plot_fig2
    global RR_interval_Canvas
    global lab
    
    if (labelled_flag == 0):
        plot_fig2 = fig2.add_subplot(111) 
        plot_fig2.clear()
        lab.config(text="RR-intervals will be displayed here", padx = 600)
        RR_interval_Canvas.show()
        
    else:
        sRt = np.size(R_t)
        y_diff = np.zeros(sRt-1)
    
        pl = np.argmin(np.abs(R_t-(ts*Fs)))
        pl2 = np.argmin(np.abs(R_t-((ts+trpd)*Fs)))
        
        for i in range (0, (sRt-1)):
            y_diff[i] = R_t[i+1] - R_t[i]
        
        y_diff = (y_diff/Fs)*1000   #Converts from sample number to millseconds
        
        x2 = range(0, (sRt-1))
        
        y_minn = np.min(y_diff)-10
        y_maxx = np.max(y_diff)+10
        x2_max = np.max(x2)
       
        plot_fig2 = fig2.add_subplot(111) 
        #Bottom Figure
        plot_fig2.clear()
        plot_fig2.plot(x2, y_diff, '*')
        plot_fig2.plot([pl+0.5, pl+0.5], [y_minn, y_maxx])
        plot_fig2.plot([pl2, pl2], [y_minn, y_maxx])
        plot_fig2.axis([0, x2_max, y_minn,y_maxx])    
        lab.config(text='', padx = 0)        
        RR_interval_Canvas.show()
        
def onclick(event):
    global bound1
    global cnt
    global invert_flag
    global R_t
    global R_amp
    global dat
   # print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
    #      (event.button, event.x, event.y, event.xdata, event.ydata))
    
    if event.button == 1:
        xx = int(event.xdata * Fs)   
        ll = np.size(R_t)
        
        if (invert_flag == 0):
            R_amp_temp = np.max(dat[xx-bound1:xx+bound1])
            pl = np.argmax(dat[xx-bound1:xx+bound1])
        else: 
            R_amp_temp = np.min(dat[xx-bound1:xx+bound1])
            pl = np.argmin(dat[xx-bound1:xx+bound1])
            
        R_t_temp = xx-(bound1+1)+pl
                      
        pl2 = np.argmin(np.abs(R_t-R_t_temp))      
        
        if (R_t_temp < R_t[pl2]):
            a = R_t[0:pl2]
            b = R_t[pl2:ll]
            
            R_t = np.append(a, R_t_temp)
            R_t = np.append(R_t, b)
            
            c = R_amp[0:pl2]
            d = R_amp[pl2:ll]
            
            R_amp = np.append(c, R_amp_temp)
            R_amp = np.append(R_amp, d)           
        else:
            a = R_t[0:pl2+1]
            b = R_t[pl2+1:ll]
            
            R_t = np.append(a, R_t_temp)
            R_t = np.append(R_t, b)   
            
            c = R_amp[0:pl2+1]
            d = R_amp[pl2+1:ll]
            
            R_amp = np.append(c, R_amp_temp)
            R_amp = np.append(R_amp, d)    
            

        draw()
        
    elif event.button == 2:
        if (invert_flag == 0):
            pl = np.argmin(np.abs(R_t-(event.xdata * Fs)))
        else:
            pl = np.argmax(np.abs(R_t-(event.xdata * Fs)))
        
        leng = np.size(R_t)
        
        a = R_t[0:pl]
        b = R_t[pl+1:leng]

        R_t = np.append(a,b)

        c = R_amp[0:pl]
        d = R_amp[pl+1:leng]
        
        R_amp = np.append(c,d)
    
        draw()
        
    elif event.button == 3: 
        xx = int(event.xdata * Fs)   
        ll = np.size(R_t)
        
        if (invert_flag == 0):
            R_amp_temp = np.min(dat[xx-bound1:xx+bound1])
            pl = np.argmin(dat[xx-bound1:xx+bound1])
            
        else: 
            R_amp_temp = np.max(dat[xx-bound1:xx+bound1])
            pl = np.argmax(dat[xx-bound1:xx+bound1])
        
        R_t_temp = xx-(bound1+1)+pl
                      
        pl2 = np.argmin(np.abs(R_t-R_t_temp))      
        
        if (R_t_temp < R_t[pl2]):
            a = R_t[0:pl2]
            b = R_t[pl2:ll]
            
            R_t = np.append(a, R_t_temp)
            R_t = np.append(R_t, b)
            
            c = R_amp[0:pl2]
            d = R_amp[pl2:ll]
            
            R_amp = np.append(c, R_amp_temp)
            R_amp = np.append(R_amp, d)           
        else:
            a = R_t[0:pl2+1]
            b = R_t[pl2+1:ll]
            
            R_t = np.append(a, R_t_temp)
            R_t = np.append(R_t, b)   
            
            c = R_amp[0:pl2+1]
            d = R_amp[pl2+1:ll]
            
            R_amp = np.append(c, R_amp_temp)
            R_amp = np.append(R_amp, d)    
            

        draw()

def onclick2(event):
    global ts 
    global trpd
    global fig2
    
    if event.button == 1:
        ss = int(event.xdata)
        ts = int(R_t[ss] / Fs)
        Jump2(ts)

def edit_toggle():
    global cid
    global fig
    global b5
    
    
    if b5.config('relief')[-1] == 'sunken':
        b5.config(relief = "raised")
        fig.canvas.mpl_disconnect(cid)

    else: 
        b5.config(relief="sunken")
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        
        
# ~~~~~~~~~~~~~~ KEY PRESS FUNCTIONS ~~~~~~~~~~~~~~~~~~~#
def leftKey(event):
    ShiftLeft()
    
def rightKey(event):
    ShiftRight()  

def Invert(event):
    global invert_flag
    invert_flag ^= 1

def shut(event):
    root.withdraw()
    sys.exit()

def shut2(event):
    sys.exit()    

def exitsave():
    swin.withdraw()
# ~~~~~~~~~~~~~~ Initialise Settings ~~~~~~~~~~~~~~~~~~~#


def int_settings():
    global colwin
    global column_number
    global dat
    global og_dat
    global cnt
    global dat
    global xint
    global yint
    global xxrange
    global k
    global xmaxx
    global xminn
    global yrange
    global yminn
    global ymaxx
    global x    
    global frq_ent
    global Fs
    
    temp = frq_ent.get()
    
    if len(temp) > 0:
        Fs = int(temp)
    
    dat = og_dat[:,(column_number-1)]
    dat = np.reshape(dat, [len(dat),1])

    x = np.arange(len(dat))
    
    cnt = int(np.size(R_t))
    xmaxx=XX
    xminn=0
    xint=XX/(xmaxx-xminn)
    ymaxx=np.max(dat[xminn:xmaxx])+0.1
    yminn=np.min(dat[xminn:xmaxx])-0.1
    yrange=ymaxx-yminn
    xxrange=xmaxx-xminn
    yint=YY/yrange
    k=0  
    colwin.withdraw()
    main_win() 

def select():
    global var
    sf = var.get()

    if (sf == 'Hilbert Transform'):
        Prediction_mode(1)
    elif(sf == 'PT'):
        Prediction_mode(2)
    elif (sf == 'Kmeans'):
        Prediction_mode(3)
    else:
        Prediction_mode(4)
        

    
def main_win():
    global var
    global entry1
    global entry2
    global scroll
    global b5
    global b6
    global root
    global fig
    global fig2
    global plot_fig
    global plot_fig2
    global graphCanvas
    global RR_interval_Canvas
    global lab
# ~~~~~~~~~~~~~~ ROOT WINDOW GENERATION ~~~~~~~~~~~~~~~~~~~#
    root = tk.Tk()
    root.title('Mc-CoCoconuts')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    
    #~~~~~~~~~~~ Keys bound to operating window ~~~~~~~~~~#
    root.bind('<Left>', leftKey)
    root.bind('<Right>', rightKey)
    root.bind('i', Invert)
    root.bind('<Escape>', shut)
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    if screen_width > 1700:
        but_wtd = 30
    else:
        but_wtd = 20
    
    # ~~~~~~~~~~~~~~ WINDOW OPTIONS / CONTROL ~~~~~~~~~~~~~~~~~~~#
    frame = tk.Frame(root)                                              #Configuration of the first frame
    frame.grid(row=0, column=1, sticky = TKc.EW, columnspan=20, rowspan = 10) #Frame position within master (i.e. root)
    frame.rowconfigure(0, weight=2)                                     #This is how the weighting resizes if the program is clicked to fullscreen
    frame.columnconfigure(1, weight=2)
    
    window = tk.Canvas(frame, relief='ridge', height = (20/27)*screen_height)              #Creating the canvas to sit within the first frame
    window.grid(row=0,column=1, sticky=TKc.NSEW, columnspan=20, rowspan = 10)         #Canvas position within frame and span of columns
    
    scroll= tk.Scrollbar(frame, orient='horizontal', command=Move)      #Creating a scrollbar within the frame
    scroll.activate('slider')                                           #Activating the scrollbar to be used as a slider type
    scroll.grid(row=11, column=1, sticky=TKc.EW, columnspan=20)          #Position of scrollbar within frame
    window.config(height = (20/27)*screen_height, xscrollcommand=scroll.set)              #Configuring canvas ('window') to be controlled in x-dimenstion by scrollbar 
    scroll.config(command=window.xview)                                 #Configuring scrollbar to update the x-view of the canvas
   
    fig = Figure(dpi=100)                                               #Configuration of the Figure to be plotted on the first canvas
    plot_fig = fig.add_subplot(111)                                     #Adding a subplot which can be updated for viewing of ECG and R-peaks
    
    graphCanvas = FigureCanvasTkAgg(fig, master=window)                 #Using TkAgg as a backend to bind the figure to the canvas
    xx = graphCanvas.get_tk_widget()    
    xx.pack(anchor=TKc.E)                                               #Positioning of figure within canvas window
    
    window.create_window((0,0), anchor = TKc.W, window=xx, width = (easterly-westerly), height = (25/36)*screen_height)       
    window.config(height = (25/36)*screen_height, scrollregion=(westerly,-(5/32)*screen_width,easterly-screen_width,0))    
    graphCanvas._tkcanvas                                               #Ensuring that "graphCanvas" can be bound to mouse input later on
    
    #Configuration of the second frame - as above
    frame2 = tk.Frame(root)                                             
    frame2.grid(row=15, column=1, columnspan=20, rowspan = 5)
    frame2.rowconfigure(0, weight=1)
    frame2.columnconfigure(1, weight=1)
    window2 = tk.Canvas(frame2, height = 250)
    window2.grid(sticky=TKc.NSEW, columnspan=20, rowspan = 5) #row=10,column=1,        
    fig2 = Figure(dpi=100)
    RR_interval_Canvas = FigureCanvasTkAgg(fig2, master=window2)
    xx2 = RR_interval_Canvas.get_tk_widget()
    xx2.grid(row=15,column=1)
    window2.create_window((0,0), anchor = TKc.NW, window=xx2, height = (25/108)*screen_height, width = (15/16)*screen_width)#, width = 1850, height = 50) #anchor = TKc.NW,
    window2.config(height=(25/108)*screen_height, width = (15/16)*screen_width, bg = 'white')
    RR_interval_Canvas._tkcanvas
    
    lab=tk.Label(frame2, text="RR-intervals will be displayed here", font = (None, 20), padx = (5/16)*screen_width, bg = 'white')
    lab.grid(row=0,column=0)
    
    
    #~~~~~~~~~~~~~~~ BUTTONS and LABELS~~~~~~~~~~~~~~~~~~~#
    
    b2 = tk.Button(root, text="<", width=3, command=ShiftLeft)
    b2.grid(row=0,column=0)
    
    b3 = tk.Button(root, text=">", width=3, command=ShiftRight)
    b3.grid(row=0,column=21)
    
    frame3 = tk.Frame(root)                                             
    frame3.grid(row=10, column=1, columnspan=20, rowspan = 5)
    frame3.rowconfigure(0, weight=1)
    frame3.columnconfigure(1, weight=1)
    
    label1=tk.Label(frame3, text="Enter start time (seconds)", anchor = TKc.W, width = but_wtd)
    label1.grid(row=0,column=0)
    entry1 = tk.Entry(frame3, width = but_wtd)
    entry1.grid(row=0,column=1, columnspan=2)
    
    label2=tk.Label(frame3, text="Enter time range per display (sec)",  anchor = TKc.W, width = but_wtd)
    label2.grid(row=1,column=0)
    entry2 = tk.Entry(frame3, width = but_wtd)
    entry2.grid(row=1,column=1, columnspan=2)

    placeholder1 = tk.Label(frame3, text=" ", anchor = TKc.E, width = int(but_wtd/4))
    placeholder1.grid(row=0,column=8)

    placeholder2 = tk.Label(frame3, text=" ", anchor = TKc.E, width = int(but_wtd/4))
    placeholder2.grid(row=0,column=8)

    bb1 = tk.Button(frame3, text = "Re-select ECG Data", width = but_wtd, padx=5, pady=2, command = column_selector2)
    bb1.grid(row=0,column=9)
    
    
    b = tk.Button(frame3, text="Update", width = int(but_wtd/2), padx=5, command=Jump)
    b.grid(row=0,column=7, rowspan=2) #sticky=TKc.
    
    
    b4 = tk.Button(frame3, text="Export Annotations", width=but_wtd, padx=5, pady=2, command=save_window)
    b4.grid(row=1,column=11) #sticky=TKc.S
    
    b5 = tk.Button(frame3, text="Edit Mode", width=but_wtd, padx=5, pady=2, command=edit_toggle, relief="raised")
    b5.grid(row=1,column=9)       
     
    b6 = tk.Button(frame3, text="Launch Prediction Mode", width=but_wtd, padx=5, pady=2, command=select, relief="raised")
    b6.grid(row=0,column=10)
    
    
    b7 = tk.Button(frame3, text="Add Pre-defined Annotation", width=but_wtd, padx=5, pady=2, command=modemenu2, relief="raised")
    b7.grid(row=0,column=11)
    
    #~~~~~~~~~~~~ Dropdown Menu for Prediction Mode ~~~~~~~~~~~~~~~~#   
    var = tk.StringVar(frame3)
    var.set('Hilbert Transform')
    choices = ['Hilbert Transform', 'PT', 'Kmeans', 'Own' ]
    
    option = tk.OptionMenu(frame3, var, *choices)
    option.grid(row=1,column=10)#, padx=10, pady=10)

    #~~~~~~~~~~~~Default Button Shortcuts~~~~~~~~~~~~~~~~#
    
    #Start Time Command Shortcuts
    but1 = tk.Button(frame3, text="60", width=5, command = lambda: Jump2(60))
    but2 = tk.Button(frame3, text="120", width=5, command = lambda: Jump2(120))
    but3 = tk.Button(frame3, text="600", width=5, command = lambda: Jump2(600))
    but4 = tk.Button(frame3, text="1200", width=5, command = lambda: Jump2(1200))
    but1.grid(row=0, column = 3)
    but2.grid(row=0, column = 4)
    but3.grid(row=0, column = 5)
    but4.grid(row=0, column = 6)
    
    
    but5 = tk.Button(frame3, text="10", width=5, command = lambda: AdjustDisplay(10))
    but6 = tk.Button(frame3, text="30", width=5, command = lambda: AdjustDisplay(30))
    but7 = tk.Button(frame3, text="60", width=5, command = lambda: AdjustDisplay(60))
    but8 = tk.Button(frame3, text="120", width=5, command = lambda: AdjustDisplay(120))
    but5.grid(row=1, column = 3)
    but6.grid(row=1, column = 4)
    but7.grid(row=1, column = 5)
    but8.grid(row=1, column = 6)
    
    
    RR_interval_Canvas.mpl_connect('button_press_event', onclick2)
    
    draw()
    
    root.mainloop()
    

modemenu()