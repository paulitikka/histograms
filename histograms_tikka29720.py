# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 10:46:49 2020

@author: pauli
"""
#Histograms
#%%Packages:
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd #for importing files
# https://pandas.pydata.org/pandas-docs/version/0.18.1/generated/pandas.DataFrame.html
import numpy as np  #for calculations, array manipulations, and fun :)
import matplotlib.pyplot as plt #for scientifical plots
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
from selenium import webdriver  # for webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, as_completed
from selenium.webdriver.common.by import By
import random
import string
import datetime
#%%#%Basic histogram for all count data first:
tot_res2=pd.read_csv('all_journals_tikka21720_ok.csv', index_col=None, header=0)
rng=tot_res2['Review Word Count']
#%import matplotlib.pyplot as plt
a = np.hstack(rng,)
_ = plt.hist(a, bins='auto')  # arguments are passed to np.histogram
plt.title("Histogram with 'auto' bins")
Text(0.5, 1.0, "Histogram with 'auto' bins")
plt.show()
#%%First plotting histograms for each journal separately, then together (regardless of year)
BMC=tot_res2.loc[tot_res2['Journal Name']=='BMC Medicine','Review Word Count']
BMJ=tot_res2.loc[tot_res2['Journal Name']=='BMJ','Review Word Count']
PLOS=tot_res2.loc[tot_res2['Journal Name']=='PLOS Medicine','Review Word Count']
#%Here is the plotting routine
plt.figure(figsize=(8,6))
plt.hist(BMC, bins=100, alpha=0.5, label="BMC Medicine")
plt.hist(BMJ, bins=100, alpha=0.5, label="BMJ")
plt.hist(PLOS, bins=100, alpha=0.5, label="PLOS Medicine")
plt.xlabel("Number of Words", size=14)
plt.ylabel("Count", size=14)
plt.title("All reviewed years for BMC, BMJ, and PLOS journals")
plt.legend(loc='upper right')
plt.savefig("overlapping_histograms_BMC_BMJ_PLOS_allyears_tikka29720.png")
#%%You may of course be interested in individual values, such as
a=len(BMC)
b=np.mean(BMC)
c=np.std(BMC)
d=np.median(BMC)
q75, q25 = np.percentile(BMC, [75 ,25])
iqr = q75 - q25
#%%
#summa=pd.concat([BMC,BMJ,PLOS])
#np.mean(summa) #521.2539510381159
#np.std(summa) #445.850452368281
#https://stackoverflow.com/questions/15315452/selecting-with-complex-criteria-from-pandas-dataframe
#%%Adding more contraints to the histograms, and plotting them one-by-one for each jorunal
ok=tot_res2['Review Word Count']<500 #this can be what you whant
ok_bmc=tot_res2['Journal Name']=='BMC Medicine'
ok_bmj=tot_res2['Journal Name']=='BMJ'
ok_plos=tot_res2['Journal Name']=='PLOS Medicine'
BMC=tot_res2.loc[ok & ok_bmc,'Review Word Count']
BMJ=tot_res2.loc[ok & ok_bmj,'Review Word Count']
PLOS=tot_res2.loc[ok & ok_plos,'Review Word Count']
#%Individual journals with certain conditions, below is for BMC:
plt.hist(BMC, bins=25, alpha=1, label="BMC journal")
plt.xlabel("Number of Words", size=14)
plt.ylabel("Count", size=14)
plt.title("All reviewed years for BMC journal less than 500 words")
plt.legend(loc='upper right')
plt.savefig("histogram_BMC_less than 500 words_allyears_tikka22720.png")
#%%Now the dates or yearly conditions:
akaasia=tot_res2.sort_values(by=['Date of Publication'])
akaasia.rename(columns={'Date of Publication':'Date'}, inplace=True)
#https://stackoverflow.com/questions/20868394/changing-a-specific-column-name-in-pandas-dataframe
akaasia['Date'] =pd.to_datetime(akaasia.Date)
#%Thrid condition, the year
#https://stackoverflow.com/questions/25146121/extracting-just-month-and-year-separately-from-pandas-datetime-column
akaasia['year'] = pd.DatetimeIndex(akaasia['Date']).year
BMC=akaasia.loc[akaasia['Journal Name']=='BMC Medicine','Review Word Count']
BMJ=akaasia.loc[akaasia['Journal Name']=='BMJ','Review Word Count']
PLOS=akaasia.loc[akaasia['Journal Name']=='PLOS Medicine','Review Word Count']
ok=akaasia['Review Word Count']<500
ok_bmc=akaasia['Journal Name']=='BMC Medicine'
ok_bmj=akaasia['Journal Name']=='BMJ'
ok_plos=akaasia['Journal Name']=='PLOS Medicine'
#%%You need to gather all the datas and conditions for the histogram multiplots first:
av1=[]
av2=np.unique(akaasia['year'])
BMCtot=[]
for i in range(len(av2)):
    av1.append(akaasia['year']==av2[i])
    BMCtot.append(akaasia.loc[ok & ok_plos & av1[i],'Review Word Count'])
#%For PLOS you need revising of this value:
av2=av2[16:]
#%%Plot the histograms together in one single plot or...
plt.figure(figsize=(8,6))
for i in range(len(BMCtot)):
    plt.hist(BMCtot[i], bins=100, alpha=0.6, label=av2[i])
plt.xlabel("Number of Words", size=14)
plt.ylabel("Count", size=14)
plt.title("All reviewed years for PLOS journal")
plt.legend(loc='upper right')
#%%Plot the histograms individually for each year in their own plot!
#The below is ok for BMC and BMJ, but for BMC you need to repeat with different values of i..:
fig, axs = plt.subplots(2, 3)
for i in range(0,3):
    axs[0, i].hist(BMCtot[i], bins=10, alpha=1, label=av2[i])
    axs[0, i].set_title(av2[i])
    fig.tight_layout(pad=3.0)
    axs[1, i].hist(BMCtot[i+3], bins=10, alpha=1, label=av2[i+3])
    axs[1, i].set_title(av2[i+3])
    fig.tight_layout(pad=3.0)
#https://kite.com/python/answers/how-to-set-the-spacing-between-subplots-in-matplotlib-in-python
#%%This is ok for PLOS separate histograms:
#fig, axs = plt.subplots(1, 2)
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.hist(BMCtot[0], bins=15, alpha=1, label=av2[0])
ax1.set_title(av2[0])
ax1.set(xlabel='Number of Words', ylabel='Count')
ax2.hist(BMCtot[1], bins=15, alpha=1, label=av2[1])
ax2.set_title(av2[1])
ax2.set(xlabel='Number of Words', ylabel='Count')
fig.tight_layout(pad=5.0)
plt.savefig("overlapping_histograms_PLOS_allyears_tikka28720v1.png")
#https://stackoverflow.com/questions/28161356/sort-pandas-dataframe-by-date
#%Thee the histograms per each year for each, perhaps overlapping better that time, but for each journal
#https://datavizpyr.com/overlapping-histograms-with-matplotlib-in-python/
#%Saving
akaasia.to_csv('all_journals_dated_tikka28720_ok.csv', index=False, na_rep='NA')
#%%Interquortile ranges for each journal in each year:
#a=len(BMC)
#b=np.mean(BMC)
#c=np.std(BMC)
#d=np.median(BMC)
#q75, q25 = np.percentile(BMC, [75 ,25])
#iqr = q75 - q25
#%
a = []
b = []
c = []
d = []
q25 = []
q75 = []
#%
av1=[]
av2=np.unique(akaasia['year'])
BMCtot=[]
for i in range(len(av2)):
    av1.append(akaasia['year']==av2[i])
    BMCtot.append(akaasia.loc[ok_bmc & av1[i],'Review Word Count'])
    #%
#    https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
#%For PLOS you need revising of BMCtot and av2 values via just deleting the rows of matrices:
#av2=av2[16:]
for i in range(len(av2)):
#    av1.append(akaasia['year']==av2[i])
    a.append(len(BMCtot[i]))
    b.append(np.round(np.mean(BMCtot[i]),1))
    c.append(np.round(np.std(BMCtot[i]),1))
    d.append(np.round(np.median(BMCtot[i]),0))
    q25.append(np.round(np.percentile(BMCtot[i], [25]),1)[0])
    q75.append(np.round(np.percentile(BMCtot[i], [75]),1)[0])
    #%
totaal=[]
totaal=pd.concat([pd.DataFrame(a),pd.DataFrame(b),pd.DataFrame(c),\
                  pd.DataFrame(d),pd.DataFrame(q25),pd.DataFrame(q75)],axis=1)   
#%%
utta=[]
akaasia2=akaasia.reset_index(drop=True)
#aka=akaasia.index[0:-1]
for i in range(len(akaasia2)-1):
#range(len(akaasia)-1):
    if akaasia2['Writers of Article'].loc[i]!=akaasia2['Writers of Article'].loc[i+1] and \
    akaasia2['Title of Article'].loc[i]!=akaasia2['Title of Article'].loc[i+1]:
        utta.append(i)
#%
utta.append(-1)
utta=list(np.sort(utta))
#utta=utta[1:]
#%
list_of_articles=[]
#%
#list_of_articles=akaasia2[0:3]
#%
#tsr=[]
for i in range(len(utta)-1):
    list_of_articles.append(akaasia2[(utta[i]+1):(utta[i+1]+1)])
#%%
#akaasia2['Number of Reviews']='nan'
#%%
#idxa = pd.Index(utta)
#tak=[]
#for i in range(len(idxa)-1):
#    if idxa[i]+1==idxa[i+1]:
#        tak.append(idxa[i])
amount_reviews=[]
for i in range(len(list_of_articles)):
    amount_reviews.append(len(list_of_articles[i]))
#    list_of_articles[i].append(amount_reviews[i])
#%Again, let's calculate all:
aa=len(amount_reviews)
a=np.round(np.mean(amount_reviews),3)
b=np.round(np.std(amount_reviews),3)
c=np.round(np.median(amount_reviews),3)
d=np.round(np.percentile(amount_reviews, [25]),5)[0]
e=np.round(np.percentile(amount_reviews, [75]),5)[0]
#%%For each: BMC
ar_bmc=[]
r_bmc=[]
for i in range(len(list_of_articles)):
    if list(list_of_articles[i].loc[:,'Journal Name'])[0]=='BMC Medicine':
        ar_bmc.append([list_of_articles[i], amount_reviews[i]])
        r_bmc.append(amount_reviews[i])
#%For each: BMJ
ar_bmj=[]
r_bmj=[]
for i in range(len(list_of_articles)):
    if list(list_of_articles[i].loc[:,'Journal Name'])[0]=='BMJ':
        ar_bmj.append([list_of_articles[i], amount_reviews[i]])
        r_bmj.append(amount_reviews[i])
#%For each: PLOS
ar_plos=[]
r_plos=[]
for i in range(len(list_of_articles)):
    if list(list_of_articles[i].loc[:,'Journal Name'])[0]=='PLOS Medicine':
        ar_plos.append([list_of_articles[i], amount_reviews[i]])
        r_plos.append(amount_reviews[i])

#%%for each journal in total
aa=len(r_plos)
a=np.round(np.mean(r_bmc),3)
b=np.round(np.std(r_bmc),3)
c=np.round(np.median(r_bmc),3)
d=np.round(np.percentile(r_bmc, [25]),3)[0]
e=np.round(np.percentile(r_bmc, [75]),3)[0]
#%% The total quantities:
pot=[]
pota=[]
for i in range(len(list_of_articles)):
    for j in range(len(av2)):
        if list(pd.DataFrame(list_of_articles[i])['year'])[0]==av2[j]:
            pot.append([av2[j],len(list_of_articles[i])]) 
pota=pd.DataFrame(pot)
yr_all=[]
for i in range(len(av2)):
    yr_all.append(list(pota.loc[pota.loc[:,0]==av2[i],1])) 
#%%for one year -> many years (in one yournal)
YR=[]
YRa=[]
av2a=[]
av2a=av2[12:] #note the change for bmj and plos
for i in range(len(ar_bmj)):
    for j in range(len(av2a)): #check the years for bmj and plos
        if list(pd.DataFrame(ar_bmj[i][0])['year'])[0]==av2a[j]:
            YR.append([av2a[j],ar_bmj[i][1]])   
YRa=pd.DataFrame(YR)
#%One can go quite long away just with pandas:
yrb=[]
for i in range(len(av2a)):
    yrb.append(list(YRa.loc[YRa.loc[:,0]==av2a[i],1]))
#%% Here you put either one journal or all yournals (i.e. yr_all/yrb)
a=[]
b=[]
c=[]
d = []
q25 = []
q75 = []
for i in range(len(yrb)):
    a.append(len(yrb[i]))
    b.append(np.round(np.mean(yrb[i]),3))
    c.append(np.round(np.std(yrb[i]),3))
    d.append(np.round(np.median(yrb[i]),3))
    q25.append(np.round(np.percentile(yrb[i], [25]),3)[0])
    q75.append(np.round(np.percentile(yrb[i], [75]),3)[0])
    #%
totaal=[]
totaal=pd.concat([pd.DataFrame(a),pd.DataFrame(b),pd.DataFrame(c),\
                  pd.DataFrame(d),pd.DataFrame(q25),pd.DataFrame(q75)],axis=1)
    

        
        