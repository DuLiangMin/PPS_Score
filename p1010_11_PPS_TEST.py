#coding=cp936
from __future__ import print_function
import pandas as pd
import numpy as np

import sys

import datetime
from dateutil.relativedelta import relativedelta
def main():
    data1 = np.loadtxt('PPS_OBS.txt')
    #print(data1)
    obs = data1[0,:]
    T_All = data1[1:,:]
    for ii in range(12):
        #print(ii)
        pre = T_All[ii,:]
        Score = TPS_SCORE_M3(obs,pre)
        print('%d'%Score)

    #print(r.shape,T_All.shape)
    #print(r==1)
    TPS_SCORE_M3(obs,pre)

def TPS_SCORE_M3(obs,pre,debug=0):
    if(debug):
        print('r=',obs)
        print(len(obs))

    r2 = expand_series(obs)
    t2 = expand_series(pre)
    if(debug):
        print('r=',obs)
        print('t=',pre)

        print('r2=',r2)
        print('t2=',t2)

    r3 = Get_Lvl(r2)
    t3 = Get_Lvl(t2)

    if(debug):
        print('r3=',r3)
        print('t3=',t3)


    A = np.array([[0,0,0],[0,1,0.8],[0,0.8,1]])
    if(debug):
        print(A)

    S = np.zeros_like(obs)
    for ii in range(len(obs)):
        S[ii] = A[r3[ii],t3[ii]]
        #print(ii+1,s)
        #print()
    if(debug):
        print('S=',S)
    #N为实况降水出现次数
    #N=sum(obs)
    #Nf = sum(pre)
    N=sum(np.where(r2>0,1,0))
    Nf=sum(np.where(t2>0,1,0))

    if(debug):
        print('N=',N)
        print('Nf=',Nf)

    if(Nf>2*N):
        if(debug):
            print('Nf>2*N')
        Score =100.*sum(S)/Nf
        #print(Score)
    else:
        if(debug):
            print('not Nf>2*N')
        Score =100.*sum(S)/N

    if(debug):
        print(Score)
    return Score



def Get_Lvl(r2):
    r3 = np.where(r2==0,1,r2)
    r3 = np.where(r2==0.5,2,r3)
    r3 = np.where(r2==1,3,r3)
    r3 = r3-1
    #print('r3=',r3)
    return r3


def expand_series(r1):
    r1 = r1.ravel() #扁平 1化
    r =r1.copy()

    for ii in range(len(r)-1):
        #print(ii)
        #print(r[ii],r[ii+1])
        if(1==r[ii] and 0==r[ii+1]):
            r[ii+1]=0.5
        if(0==r[ii] and 1==r[ii+1]):
            r[ii]=0.5

    return r









if __name__ == "__main__":
    main()
