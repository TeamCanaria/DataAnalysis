#Shared Library
import numpy as np


def acc(TP, FP, FN):
    y = np.true_divide(TP,(TP+FP+FN))*100
    return y 

def acc2(TP, FP, FN):
    sen = np.true_divide(TP, (TP+FN))*100
    posp = np.true_divide(TP, (TP+FP))*100

    return sen, posp

#Acc check for created data      
def test(R_pred, R_act, thr):
    err = 0.1
    counter = 1
    
    R_pred = R_pred[:]
    R_act = R_act[:]
    
    if (len(R_pred) == 1):
        R_pred = np.transpose(R_pred)
        
    if (len(R_act) == 1):
        R_act = np.transpose(R_act)

    lp = len(R_pred)
    lr = len(R_act)

    i = 0
    j = 0
    TP = 0;         # True positive - Correctly Predicted QRS peak (within accuracy of given frequency)
    FP = 0;         # False positive - Idenification of a Peak which is not a peak
    FN = 0;         # Missing the identification of a peak  
    
    while((i<lp-1) & (j<lr-1)):
        
        if ((R_pred[i] >= (R_act[j]-thr-err)) & (R_pred[i] <= (R_act[j]+thr+err))):
            TP += 1
            i += 1
            j += 1
            
        elif(R_pred[i] > (R_act[j]-err)):
            FN += 1
            j += 1
            
        elif(R_pred[i] < (R_act[j]+err)): 
            FP += 1
            i += 1
            
        else:
            print('Error')
            
        counter += 1
    
    return TP, FP, FN

def test2(R_pred, R_act, thr):
    TP = 0;          # True positive - Correctly Predicted QRS peak (within accuracy of given frequency         % False positive - Idenification of a Peak which is not a peak
    FN = 0;          # Missing the identification of a peak
    
    M = len(R_pred)
    flag = 0
    marker = np.zeros(M)
    
    for i in range(len(R_act)):    

        j=0
        test = R_act[i]
        compare = R_pred[j]

        while (j < M):
            flag = 0
            
            edge1 = test-thr
            edge2 = test+thr
            if (compare > edge1):
                if (compare < edge2):
                    TP = TP + 1
                    marker[j] = 1
                    j = M-1
                    flag = 1
                
            compare = R_pred[j]
            j = j +1
        
        if (flag != 1):
            FN = FN + 1
            flag = 1
    
    marker = marker[marker!=1]
    
    FP = len(marker)

    return TP, FP, FN