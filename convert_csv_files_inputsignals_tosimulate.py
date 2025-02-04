import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import csv
from numpy.fft import fft

def datos_componente(nombre_archivo,n):
    data = []
    with open(nombre_archivo, 'r') as file: 
        csv_reader = csv.reader(file, quotechar='"')
        for row in csv_reader:
            aux = []
            for i in range(0, len(row)):
                aux.append(float(row[i]))
            data.append(aux)
    file.close()
    
    freq=[]
    data_res=[]
    for i in range(len(data)):
        freq.append(data[i][0])
        data_res.append(data[i][1])
        
    xdup_freq = freq
    ydup_dat = data_res
    i_dat=[]
    for i in xdup_freq:
        while(xdup_freq.count(i) > 1):
            xdup_freq.remove(i)
            i_dat.append(xdup_freq.index(i))
    for i in range(len(i_dat)):
        ydup_dat.remove(ydup_dat[i_dat[i]]) 
        
    x = xdup_freq
    y = ydup_dat
    f1 = interp1d(x, y, kind='nearest')
    xx = np.linspace(10,20,n)#np.linspace(min(x),max(x),n)
    
    return freq, data_res,xdup_freq,ydup_dat,xx,f1(xx)

def sparams_to_power(values,n):
    transf_val=[]
    for i in range(n):
        transf_val.append(pow(10,(values[i]/10)))
    return transf_val

def datos_simulados_RI(n,rl_hyb,IL_hyb,IL_omt,RL_omt,RL_feedhorn,RL_window,gain_LNA,RL_load,Tn_lna):
    
    ## DATOS TOMADOS DE LAS SIMULACIONES EN CST DE LA TESIS DE PAZ, PARA OMT, HIBRIDO Y FEEDHORN
    ### n SIGNIFICA QUE TENDREMOS 200 DATOS DESDE 10 A 20 GHz
    # DATOS DEL HYB
    freq1, data_res1,xdup_freq1,ydup_dat1,xx1,data_RL_hyb=datos_componente(rl_hyb,n) #rl
    freq2, data_res2,xdup_freq2,ydup_dat2,xx2,data_IL_hyb=datos_componente(IL_hyb,n) #il

    # DATOS DEL OMT
    freq3, data_res3,xdup_freq3,ydup_dat3,xx3,data_IL_omt=datos_componente(IL_omt,n) #il
    freq4, data_res4,xdup_freq4,ydup_dat4,xx4,data_RL_omt=datos_componente(RL_omt,n) #rl

    # DATOS DEL FEEDHORN
    freq5, data_res5,xdup_freq5,ydup_dat5,xx5,data_RL_FH =datos_componente(RL_feedhorn,n) #rl
    #dtos de la ventana
    freq6, data_res6,xdup_freq6,ydup_dat6,xx6,data_RL_W =datos_componente(RL_window,n) #rl
    #dtos de gain lna
    freq7, data_res7,xdup_freq7,ydup_dat7,xx7,data_gain_lna =datos_componente(gain_LNA,n) #rl
     #dtos de load
    freq8, data_res8,xdup_freq8,ydup_dat8,xx8,data_RL_load =datos_componente(RL_load,n) #rl
     #dtos de tnoise lna
    freq9, data_res9,xdup_freq9,ydup_dat9,xx9,data_tnoise_lna =datos_componente(Tn_lna,n) #rl

    #conversion de los datos de la tesis de paz en db a potencia [W]
    new_rl_hyb_real=sparams_to_power(data_RL_hyb,n)
    new_il_hyb_real=sparams_to_power(data_IL_hyb,n)
    new_rl_omt_real=sparams_to_power(data_RL_omt,n)
    new_il_omt_real=sparams_to_power(data_IL_omt,n)
    new_rl_fh_real=sparams_to_power(data_RL_FH,n)
    new_rl_w_real=sparams_to_power(data_RL_W,n)
    new_gain_lna_real=sparams_to_power(data_gain_lna,n)
    new_rl_load_real=sparams_to_power(data_RL_load,n)

    ## para simular que pasa si tenemos valores de IL OMT E IL HYB divididos entre 2
    Q=[]
    W=[]
    E=[]
    R=[]
    for i in range(n):
        Q.append(new_il_omt_real[i]/5)# 0.1
        W.append(new_il_omt_real[i]/10)# 0.05
        E.append((new_il_omt_real[i]/150)+0.0002)##0.003
        R.append(new_il_omt_real[i]/50)##0.01
    Q2=[]
    W2=[]
    E2=[]
    R2=[]
    for i in range(n):
        Q2.append(1-pow(10,(-Q[i]/10)))# 
        W2.append(1-pow(10,(-W[i]/10)))#
        E2.append(1-pow(10,(-E[i]/10)))#
        R2.append(1-pow(10,(-R[i]/10)))#
    Z=new_rl_w_real
    X=new_rl_omt_real
    C=new_rl_hyb_real
    V=new_rl_fh_real
    M=new_rl_load_real
    N=new_gain_lna_real
    U=data_tnoise_lna
    
    return Q2,W2,E2,R2,Z,X,C,V,xx1,data_RL_W,data_RL_FH,data_RL_omt,data_IL_omt,data_IL_hyb,data_RL_hyb,data_gain_lna, N,M,data_RL_load,U,Q,W,E,R



