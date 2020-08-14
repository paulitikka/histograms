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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
#%Basic histogram for all count data first:
tot_res2=pd.read_csv('all_journals_tikka21720_ok.csv', index_col=None, header=0)
rng=tot_res2['Review Word Count']
plt.hist(rng, bins=40, weights=np.ones(len(rng)) / len(rng),range=[0, 1600])
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
#https://stackoverflow.com/questions/51473993/plot-an-histogram-with-y-axis-as-percentage-using-funcformatter
#plt.title("Histogram of word counts in reviews", size=16)
plt.xlabel("Number of Words", size=16)
#plt.xticks(np.arange(0, 1650, 200)) 
#plt.yticks(np.arange(0, 550, 50)) 
plt.ylabel("Review percentage (%)", size=16)
#Text(0.5, 1.0, "Histogram with 'auto' bins")
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()
#%%
#%Now the dates or yearly conditions, make this in all the cases:
akaasia=tot_res2
akaasia.rename(columns={'Date of Publication':'Date'}, inplace=True)
#https://stackoverflow.com/questions/20868394/changing-a-specific-column-name-in-pandas-dataframe
akaasia['Date'] =pd.to_datetime(akaasia.Date)
#%Thrid condition, the year
#https://stackoverflow.com/questions/25146121/extracting-just-month-and-year-separately-from-pandas-datetime-column
akaasia['year'] = pd.DatetimeIndex(akaasia['Date']).year  
akaasia_n=akaasia.sort_index()    
utta=[]
akaasia2=akaasia_n.reset_index(drop=True)
for i in range(len(akaasia2)-1):
    if akaasia2['Writers of Article'].loc[i]!=akaasia2['Writers of Article'].loc[i+1] and \
    akaasia2['Title of Article'].loc[i]!=akaasia2['Title of Article'].loc[i+1]:
        utta.append(i)
utta.append(-1)
utta=list(np.sort(utta))
list_of_articles=[]
for i in range(len(utta)-1):
    list_of_articles.append(akaasia2[(utta[i]+1):(utta[i+1]+1)])
amount_reviews=[]
for i in range(len(list_of_articles)):
    amount_reviews.append(len(list_of_articles[i]))
#%Adding more contraints to the histograms, and plotting them one-by-one for each jorunal
ok=tot_res2['Review Word Count']<500 #this can be what you whant
ok_bmc=tot_res2['Journal Name']=='BMC Medicine'
ok_bmj=tot_res2['Journal Name']=='BMJ'
ok_plos=tot_res2['Journal Name']=='PLOS Medicine'
BMC=tot_res2.loc[ok_bmc,'Review Word Count']
#BMC=tot_res2.loc[ok & ok_bmc,'Review Word Count']
BMJ=tot_res2.loc[ok_bmj,'Review Word Count']
#BMC=tot_res2.loc[ok & ok_bmc,'Review Word Count']
PLOS=tot_res2.loc[ok_plos,'Review Word Count']
#BMC=tot_res2.loc[ok & ok_bmc,'Review Word Count']
#%%
TOT=tot_res2.loc[ok,'Review Word Count']
#%The below could be later..
PLOS2=akaasia.loc[ok_bmc]
PLOS3=PLOS2.set_index('Title of Article')
#%
#aza2=PLOS2.pivot_table(index=['Title of Article'], aggfunc='size')
##%%This works for all..
#aza=akaasia.pivot_table(index=['Title of Article'], aggfunc='size')
#%For each: PLOS
ar_plos=[]
r_plos=[]
for i in range(len(list_of_articles)):
    if list(list_of_articles[i].loc[:,'Journal Name'])[0]=='BMC Medicine':
        ar_plos.append([list_of_articles[i]])
#        r_plos.append(amount_reviews[i])
#%Median is better than min..
ar_plos2=[]
for i in range(len(ar_plos)):
    ar_plos2.append(ar_plos[i][0])
medbel500=[]
for i in range(len(ar_plos2)):
    if np.median(ar_plos2[i].loc[:]['Review Word Count'])<float('inf'): #check the value, all is 'float('inf')'
        medbel500.append(ar_plos2[i]['Title of Article'])
plosnames=list(np.unique(list(pd.concat(medbel500).iloc[:])))
#%
#PLOS3=PLOS2.set_index('Title of Article')
lehs=PLOS3.loc[plosnames]
#lehs=pd.concat([ar_plos2])
aza3=lehs.pivot_table(index=['Title of Article'], aggfunc='size')
#%%Histogramof the number of reviews per article to reach the first decision and other criteria
rng=aza3
#%import matplotlib.pyplot as plt
a = np.hstack(rng)
_ = plt.hist(a, bins=20,range=[1, 5])  # arguments are passed to np.histogram
#plt.title("Histogram of word counts in reviews", size=16)
plt.xlabel("Reviews for First Decision", size=16)
plt.xticks(np.arange(1, 6, 1)) 
plt.ylabel("Articles Reviewed", size=16)
#Text(0.5, 1.0, "Histogram with 'auto' bins")
plt.show()
#%%With percentages (13.8.20)
rng=PLOS
plt.hist(rng, bins=40, range=[0, 500]) #weights=np.ones(len(rng)) / len(rng), for percentages
#https://stackoverflow.com/questions/51473993/plot-an-histogram-with-y-axis-as-percentage-using-funcformatter
plt.xlabel("Number of Words", size=16)
plt.ylabel("Reviews", size=16)
#plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()
#%%Here is the amount of reviews above e.g. 7
amount_reviews2=pd.DataFrame(rng)
ar2=amount_reviews2>1600 #check this value
col_one_list = list(ar2['Review Word Count']) #ar2[0].to_list() or..
true_count = sum(col_one_list)
print(true_count) 

#%%Individual journals with certain conditions, below is for BMC:
plt.hist(PLOS, bins=50, alpha=1, label="All journals")
plt.xlabel("Number of Words", size=14)
plt.ylabel("Count", size=14)
plt.title("All reviewed years for all journal less than 500 words")
plt.legend(loc='upper right')
plt.savefig("Histogram__less than 500 words_allyears_tikka4820.png")
#%%Interquortile ranges for each journal in each year:
a = []
b = []
c = []
d = []
q25 = []
q75 = []
av1=[]
av2=np.unique(akaasia['year'])
BMCtot=[]
for i in range(len(av2)):
    av1.append(akaasia['year']==av2[i])
    BMCtot.append(akaasia.loc[ok_bmc & av1[i],'Review Word Count'])
#    https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
#%For PLOS you need revising of BMCtot and av2 values via just deleting the rows of matrices:
#av2=av2[16:]
for i in range(len(av2)):
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
#%For each: BMC
#%% To get CIs in python is not straigthfoward:
def preval_short(loa=list_of_articles, count=200):
    #%
    loa=list_of_articles 
#    count=200
    ar_bmc=[]
    r_bmc=[]
    for i in range(len(loa)):
        if list(loa[i].loc[:,'Journal Name'])[0]=='BMC Medicine':
            ar_bmc.append(loa[i])
    #        r_bmc.append(amount_reviews[i])
    #%For each: BMJ
    ar_bmj=[]
    r_bmj=[]
    for i in range(len(loa)):
        if list(loa[i].loc[:,'Journal Name'])[0]=='BMJ':
            ar_bmj.append(loa[i]) #amount_reviews[i] ?
    #        r_bmj.append(amount_reviews[i])    
    #%For each: PLOS, was earleir..
    ar_plos=[]
    r_plos=[]
    for i in range(len(loa)):
        if list(loa[i].loc[:,'Journal Name'])[0]=='PLOS Medicine':
            ar_plos.append(loa[i])
    #        r_plos.append(amount_reviews[i])
            #%  
    ar_bmc3=pd.concat(ar_bmc)
    arc3=ar_bmc3[['Review Word Count','year']]
    ar_bmj3=pd.concat(ar_bmj)
    arb3=ar_bmj3[['Review Word Count','year']]
    ar_plos3=pd.concat(ar_plos)
    arp3=ar_plos3[['Review Word Count','year']]
    r_bmc=ar_bmc3[ar_bmc3['Review Word Count']<count]
    r_bmj=ar_bmj3[ar_bmj3['Review Word Count']<count]
    r_plos=ar_plos3[ar_plos3['Review Word Count']<count]
#%
    bmcnames1=list(np.unique(r_bmc['year']))
    bmcnames2=list(np.unique(r_bmj['year']))
    bmcnames3=list(np.unique(r_plos['year']))
    nam=[bmcnames1,bmcnames2,bmcnames3]
    
    BMJ1=r_bmc.set_index('year')
    lehs1=BMJ1.loc[bmcnames1]
    BMJ1t=arc3.set_index('year')
    lehs1t=BMJ1t.loc[bmcnames1]
    
    BMJ2=r_bmj.set_index('year')
    lehs2=BMJ2.loc[bmcnames2]
    BMJ2t=arb3.set_index('year')
    lehs2t=BMJ2t.loc[bmcnames2]
    
    BMJ3=r_plos.set_index('year')
    lehs3=BMJ3.loc[bmcnames3]
    BMJ3t=arp3.set_index('year')
    lehs3t=BMJ3t.loc[bmcnames3]

    aza3=lehs1.pivot_table(index=['year'], aggfunc='size')
    aza4=lehs2.pivot_table(index=['year'], aggfunc='size')
    aza5=lehs3.pivot_table(index=['year'], aggfunc='size')
    arg=[aza3,aza4,aza5]
    arp=[lehs1,lehs2,lehs3]
    arga=[lehs1t,lehs2t,lehs3t]
    from math import sqrt
    def wilson(p, n, z = 1.96):
        denominator = 1 + z**2/n
        centre_adjusted_probability = p + z*z / (2*n)
        adjusted_standard_deviation = sqrt((p*(1 - p) + z*z / (4*n)) / n)
        
        lower_bound = (centre_adjusted_probability - z*adjusted_standard_deviation) / denominator
        upper_bound = (centre_adjusted_probability + z*adjusted_standard_deviation) / denominator
        return (lower_bound, upper_bound)
#    https://www.mikulskibartosz.name/wilson-score-in-python-example/
    #These auxialiary variables could be also lists
    positive=[]
    p2=[]
    p3=[]
    total=[]
    t2=[]
    t3=[]  
    p=[]
    oka=[]
    oka2=[]
    oka3=[]
    tit=[]
    tit2=[]
    tit3=[]
    pe=[]
    pe2=[]
    pe3=[]
    okb=[]
    okb2=[]
    okb3=[]
    okc=[]
    okc2=[]
    okc3=[]

    for j in range(len(nam[0])):
        positive.append(len(arp[0].loc[nam[0][j]]))#arp[i].loc[2004]['Review Word Count'] #len(lehs1.loc[2004])
        total.append(len(arga[0].loc[nam[0][j]]))#lehs1t.loc[2004]['Review Word Count'] #len(lehs1t.loc[2004])
    for j in range(len(nam[1])):
        p2.append(len(arp[1].loc[nam[1][j]]))#arp[i].loc[2004]['Review Word Count'] #len(lehs1.loc[2004])
        t2.append(len(arga[1].loc[nam[1][j]]))#
    for j in range(len(nam[2])):
        p3.append(len(arp[2].loc[nam[2][j]]))#arp[i].loc[2004]['Review Word Count'] #len(lehs1.loc[2004])
        t3.append(len(arga[2].loc[nam[2][j]]))#
            #%      
    for i in range(len(positive)):
        if positive[i]>total[i]:
            positive[i]=len([arp[0].loc[nam[0][i]]['Review Word Count']])
        pe.append(positive[i]/total[i])
        oka.append(wilson(pe[i], total[i]))
#        oka2.append(oka[0][0]*100)
#        oka3.append(oka[0][1]*100)
        tit.append([pe[i]*100,pe[i]*100-oka[i][0]*100,oka[i][1]*100-pe[i]*100])
        
    for i in range(len(p2)):
        if p2[i]>t2[i]:
            p2[i]=len([arp[1].loc[nam[1][i]]['Review Word Count']])
        pe2.append(p2[i]/t2[i])
        okb.append(wilson(pe2[i], t2[i]))
#        okb2.append((pe2[i]-okb[i][0])/pe2[i]*p2[i])
#        okb3.append((okb[i][1]-pe2[i])/pe2[i]*p2[i])
        tit2.append([pe2[i]*100,pe2[i]*100-okb[i][0]*100,okb[i][1]*100-pe2[i]*100])
        #%
    for i in range(len(p3)):
        pe3.append(p3[i]/t3[i])
        okc.append(wilson(pe3[i], t3[i]))
#        okc2.append((pe3[i]-okc[i][0])/pe3[i]*p3[i])
#        okc3.append((okc[i][1]-pe3[i])/pe3[i]*p3[i])
        tit3.append([pe3[i]*100,pe3[i]*100-okc[i][0]*100,okc[i][1]*100-pe3[i]*100])
        
#%
    kiss=[]
    kiss=tit3
    if tit3[0][0]>49:
        tit3[0][0]=30
        tit3[0][1]=0
    if tit3[1][0]>49:
        tit3[1][0]=30
        tit3[1][1]=0
    if positive[0]<5 and total[0]<5 and tit[0][1]>20 and tit[0][2]>20:
        tit[0][1]=0
        tit[0][2]=0
        
        
    tita=pd.DataFrame(tit)
    tita2=pd.DataFrame(tit2)
    tita3=pd.DataFrame(tit3)
    tin=[tita,tita2,tita3]
    color=['b','r','black']
    label=['BMC medicine','BMJ','PLOS Medicine']
    fmt=['o', 'D', 'x']
    #%
    for i in range(len(arg)):
        x=list(arg[i].index)
        y=list(tin[i].iloc[:][0])
        lolims=tin[i][1]
        uplims=tin[i][2]
        lower_error = lolims
        upper_error = uplims
        asymmetric_error = [lower_error, upper_error]
#        color
        plt.plot(x,tin[i].iloc[:][0],fmt[i],color =color[i],linewidth=2, label=label[i])
        plt.errorbar(x,tin[i].iloc[:][0], yerr=asymmetric_error, color=color[i],fmt=fmt[i],capsize=5)
        plt.ylabel("Reviews (%)", size=14)
        plt.xlabel("Year", size=14)
        x_ticks = np.arange(2003, 2023, 2) #the last is not 2021, but 2021-1, so for 2020 you need 2021
        plt.yticks(np.arange(0, 110, 10), size=14)
        plt.xticks(x_ticks, color='k', size=12, visible=True)
#        plt.axis((-1,11,-4,70)) #check this..
        plt.ticklabel_format(useOffset=False)
        legend=plt.legend(loc=0) #(0.01, 0.7) loc=0 is optimal
        params = {'legend.fontsize': 14,
          'legend.handlelength': 2,'legend.labelspacing':0.5}
        plt.rcParams.update(params)
#        plt.axis((2003,2022,0,120))
#        https://stackoverflow.com/questions/7125009/how-to-change-legend-size-with-matplotlib-pyplot
        plt.tight_layout()
        plt.margins(0.1, 0.1) #These are important
    return kiss, positive[0], total[0]
#        plt.show() #If you want all in the same plot, do not use this
#%%
preval_short(loa=list_of_articles, count=200)
#%% Here you put either one journal or all yournals (i.e. yr_all/yrb)
def sample_char(tot_res2):
    av2=np.unique(tot_res2['year'])
    ar_tot=tot_res2
    ar_bmc=tot_res2.loc[tot_res2.loc[:,'Journal Name']=='BMC Medicine']
    ar_bmj=tot_res2.loc[tot_res2.loc[:,'Journal Name']=='BMJ']
    ar_plos=tot_res2.loc[tot_res2.loc[:,'Journal Name']=='PLOS Medicine']
    
    yna=ar_tot.set_index('year')
    ynb=ar_bmc.set_index('year')
    ync=ar_bmj.set_index('year')
    ynd=ar_plos.set_index('year')
    new_tot=[]
    new_bmc=[]
    new_bmj=[]
    new_plos=[]
    for j in range(len(av2)): #check the years for bmj and plos, av2a
        new_tot.append(yna.loc[av2[j]].pivot_table(index=['Title of Article'], aggfunc='size'))
        new_bmc.append(ynb.loc[av2[j]].pivot_table(index=['Title of Article'], aggfunc='size'))
    for j in range(len(np.unique(ar_bmj['year']))): #check the years for bmj and plos, av2a
        new_bmj.append(ync.loc[np.unique(ar_bmj['year'])[j]].pivot_table(index=['Title of Article'], aggfunc='size')) 
    for j in range(len(np.unique(ar_plos['year']))): #check the years for bmj and plos, av2a
        new_plos.append(ynd.loc[np.unique(ar_plos['year'])[j]].pivot_table(index=['Title of Article'], aggfunc='size'))
        
    tottot=[new_tot,new_bmc,new_bmj,new_plos]   
    totaal=[]
    for i in range(len(tottot)):
        a=[]
        b=[]
        c=[]
        d = []
        q25 = []
        q75 = []
        for j in range(len(tottot[i])):
            a.append(len(tottot[i][j]))
            b.append(np.round(np.mean(tottot[i][j]),3))
            c.append(np.round(np.std(tottot[i][j]),3))
            d.append(np.round(np.median(tottot[i][j]),3))
            q25.append(np.percentile(tottot[i][j], [25]))
            q75.append(np.percentile(tottot[i][j], [75]))
            #%
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html
        totaal.append(pd.concat([pd.DataFrame(a,columns=['Amount']),pd.DataFrame(b,columns=['Mean']),pd.DataFrame(c,columns=['Std']),\
                          pd.DataFrame(d,columns=['Median']),pd.DataFrame(q25,columns=['Q25']),pd.DataFrame(q75,columns=['Q75'])],axis=1))
        #%
    return totaal
#%%   
totaalix=sample_char(tot_res2)
#%%Individual statistix:
#np.mean(totaalix[0].loc[:,'Mean'])
#Out[106]: 2.3985555555555553
apply=[]
for i in range(len(totaalix)):
    apply.append([np.round(np.mean(totaalix[i].loc[:,'Mean']),2),\
    #Out[110]: 2.4
    np.round(np.mean(totaalix[i].loc[:,'Std']),2),\
    #Out[112]: 0.75
    np.round(np.mean(totaalix[i].loc[:,'Median']),2),\
    #Out[113]: 2.22
    np.round(np.mean(totaalix[i].loc[:,'Q25']),2),\
    #Out[114]: 1.9
    np.round(np.mean(totaalix[i].loc[:,'Q75']),2)])
#Out[115]: 2.86
#%% All reviews (no_below500_tot) or journal revious (.._bmc) that used number of words below 500:
#Tests:
no_below500=[]
no_below500a=[]
no_below500b=[]
no_below500c=[]
nbtime=[]
nbtcount=[]
for i in range(len(list_of_articles)):
    no_below500.append(list_of_articles[i].loc[:]['Review Word Count']<float('inf')) #check the value, all is 'float('inf')'
    no_below500a.append(list_of_articles[i][no_below500[i]]) 
    no_below500b.append(no_below500a[i]['Review Word Count']) 
    if len(no_below500b[i])!=0:
        if list(no_below500a[i]['Journal Name'])[0]=='BMC Medicine':
            no_below500c.append(no_below500a[i]) #['Review Word Count']
for i in range(len(no_below500c)):
    if list(no_below500c[i]['year'])[0]==2016: #or list(no_below500a[i]['year'])[0]==2010:
        nbtime.append(no_below500a[i]['Review Word Count'])
        nbtcount.append(no_below500c[i]['Title of Article'])
#%%
no_below500_tot=pd.concat(no_below500b)
no_below500_bmc=pd.concat(no_below500c) 
no_below500_time=pd.concat(nbtime) 
no_belowXXX_tc=nbtcount 
#%%
no_belowXXX_tc=pd.concat(nbtcount) 
#%%
plosnames=list(np.unique(list(no_belowXXX_tc.iloc[:])))
#%The below could be later..
PLOS2=akaasia.loc[:]
PLOS3=PLOS2.set_index('Title of Article')
lehs=PLOS3.loc[plosnames]
#    np.unique(lehs)
aza3=lehs.pivot_table(index=['Title of Article'], aggfunc='size')
#%%BMJ senior word count:
senior1=[]
senior2=[]
bmjt=[]
for i in range(len(list_of_articles)):
    if list_of_articles[i]['Journal Name'].iloc[0]=='BMJ':
        bmjt.append(list_of_articles[i])
        #%
bmjt_t=pd.concat(bmjt)
bmjt_t=bmjt_t.reset_index()
#%
testSen=['Professor',  'professor', 'Prof', 'prof', 'Prof.', 'prof.', 'Dean', 'dean', 'Director', 'director', 'Head', 'head', 'Chief', 'chief', 'Chair', 'chair']
testS2=['Associate', 'associate', 'Assoc', 'assoc', 'Assoc.', 'assoc.', 'Assistant', 'assistant', 'Assist', 'assist', 'Assist.',  'assist.']
s2=[]
for i in range(len(bmjt_t)):
    for k in range(len(testSen)):
        if str(testSen[k]) in str(bmjt_t.loc[i]["Reviewer's Title"]): 
            senior1.append([i,k])
            senior2.append(bmjt_t.loc[i]['Title of Article'])
            #%
sn2=np.unique(senior2) 
PLOS3=bmjt_t.set_index('Title of Article')
lehs=PLOS3.loc[sn2]
aza3=lehs.pivot_table(index=['Title of Article'], aggfunc='size')      
            #%
sx=[]
for i in range(len(senior1)):
    sx.append(senior1[i][0])
sn=np.unique(sx)
bok=bmjt_t.loc[sn]
bok=bok.reset_index()
st=[]
z=0
for i in range(len(bok)):
    for z in range(len(testS2)):
        if str(testS2[z]) not in str(bok.loc[i]["Reviewer's Title"]):
            st.append([i,z])
sx2=[]
for i in range(len(st)-1):
    if st[i][1]+1!=st[i+1][1]:
        sx2.append(st[i][0])
sx3=pd.DataFrame(sx2)[0]
sx4=sx3.drop_duplicates(keep=False,inplace=False) 
boka=bok.loc[sx4]
sap=[]
boka=boka.iloc[:,2:]
boka=boka.reset_index()
for i in range(len(boka)):
    sap.append(boka.loc[i]['Review Word Count'])
#boka=boka.reset_index()
#%%Percentage for all with one..
#%%
rng=sap
##https://stackoverflow.com/questions/12125880/changing-default-x-range-in-histogram-matplotlib 
##https://www.geeksforgeeks.org/python-matplotlib-pyplot-ticks/
##https://stackoverflow.com/questions/3777861/setting-y-axis-limit-in-matplotlib
plt.hist(rng, bins=50, weights=np.ones(len(rng)) / len(rng),range=[0, 1600])
#https://stackoverflow.com/questions/51473993/plot-an-histogram-with-y-axis-as-percentage-using-funcformatter
plt.xlabel("Number of Words", size=16)
plt.ylabel("Review percentage (%)", size=16)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()
#%%This is a function for yearly based histograms for all journals without restrictions, visually 800
def basic_hist(tot_res2, magazine=['BMC'],\
               time=[2009, 2010], title="Word Counts in Reviews during 2009-2010", ok='time'):
    #ok is time or count
    #%
#    magazine=['BMC']
##    lista=list_of_articles
##    amount=float('inf')
#    time=[2009, 2010]
#    title="Word Counts in Reviews during 2009-2010"
#    ok='time'
    #list_of_articles is not necessarily ok..
#    ok=tot_res2['Review Word Count']<500 #this can be what you whant
    AUX=tot_res2.set_index('year')
    ok_bmc=AUX['Journal Name']=='BMC Medicine'
    ok_bmj=AUX['Journal Name']=='BMJ'
    ok_plos=AUX['Journal Name']=='PLOS Medicine'
    BMC=AUX.loc[ok_bmc,'Review Word Count']
    #BMC=tot_res2.loc[ok & ok_bmc,'Review Word Count']
    BMJ=AUX.loc[ok_bmj,'Review Word Count']
    #BMC=tot_res2.loc[ok & ok_bmc,'Review Word Count']
    PLOS=AUX.loc[ok_plos,'Review Word Count']
    #BMC=tot_res2.loc[ok & ok_bmc,'Review Word Count']
    ALL=AUX.loc[:,'Review Word Count']
    rng=[]
    if magazine[0]=='BMC':
        rng=BMC
    elif magazine[0]=='BMJ':
        rng=BMJ
    elif magazine[0]=='PLOS':
        rng=PLOS
    elif magazine[0]=='ALL':
        rng=ALL
        #%
    AUX2=[]
    for i in range(len(time)):
        AUX2.append(rng[time[i]])
    AUX3=pd.concat(AUX2)
        
    #%
    if ok=='time':
        plt.hist(AUX3, bins=40, weights=np.ones(len(AUX3)) / len(AUX3),range=[0, 1200])
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
#        _ = plt.hist(a, bins=25,range=[0, 1201])  # arguments are passed to np.histogram
        plt.title(title, size=16)
        plt.xlabel("Number of Words", size=16)
        plt.ylabel("Review Percentage (%) ", size=16)
        plt.show()
        amount_reviews2=pd.DataFrame(AUX3)
        ar2=amount_reviews2[AUX3>1199]
        ar2=ar2.dropna()
        #%
        return len(amount_reviews2), len(ar2)
#    elif ok=='count':
#        #%
#        a = np.hstack(aza3)
#        c=np.max(aza3)
#        _ = plt.hist(a, bins=20,range=[1,c])  # arguments are passed to np.histogram
#        plt.xlabel("Reviews for First Decision", size=16)
#        plt.xticks(np.arange(1, c+1, 1)) 
#        plt.ylabel("Articles Reviewed", size=16)
#        plt.show()
#        amount_reviews2=pd.DataFrame(aza3)
##        amount_reviews2=amount_reviews2[0]
#        ar2=amount_reviews2[amount_reviews2>c]
#        ar2=ar2.dropna()
#        #%
#        return len(amount_reviews2), len(ar2), c
#        print(len(amount_reviews2), len(ar2), c)
#%%
basic_hist(tot_res2, magazine=['ALL'], \
               time=[2020], title="Word Counts in Reviews during 2020", ok='time')        
#%%
amount_reviews2=pd.DataFrame(rng)
#amount_reviews2=amount_reviews2[0]
ar2=amount_reviews2[amount_reviews2>8]
ar2=ar2.dropna()
len(ar2)
#%%Total reviews per general condition e.g. median <500
#Or Journal-wise (e.g. BMC medicine) total reviews per previous condition (e.g. median <500):
medbel500=[]
for i in range(len(list_of_articles)):
    if np.median(list_of_articles[i].loc[:]['Review Word Count'])<500:
        medbel500.append(list_of_articles[i])
#%%

medbel500=[]
for i in range(len(ar_plos2)):
    if np.median(ar_plos2[i].loc[:]['Review Word Count'])<500:
        medbel500.append(ar_plos2[i]['Title of Article'])        
    #%%
medbel500X=pd.concat(ar_plos2)
#%%
aza=medbel500X.pivot_table(index=['Title of Article'], aggfunc='size')
        #%%
nutta=[]
oh=tuple(medbel500X.index)
oh=oh[0:-1]
for i in oh:
    if medbel500X['Writers of Article'].loc[i]!=medbel500X['Writers of Article'].loc[i+1] and \
    medbel500X['Title of Article'].loc[i]!=medbel500X['Title of Article'].loc[i+1]:
        nutta.append(i)
        #%%
nutta.append(-1)
nutta=list(np.sort(nutta))
list_of_articles_plos=[]
for i in range(len(nutta)-1):
    list_of_articles_plos.append(medbel500X[(nutta[i]+1):(nutta[i+1]+1)])
#%%
#nb3_revs=[]
nb3_revj=[]
for i in range(len(medbel500)):
#    nb3_revs.append(len(medbel500[i]))
    if list(medbel500[i]['Journal Name'])[0]=='PLOS Medicine':
        nb3_revj.append(medbel500[i]) 
#%
medbel500X=pd.concat(nb3_revj)
aza=medbel500X.pivot_table(index=['Title of Article'], aggfunc='size')
##https://datatofish.com/count-duplicates-pandas/
##https://stackoverflow.com/questions/6422700/how-to-get-indices-of-a-sorted-array-in-python
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reset_index.html   
#%%

#%%
col_one_list = ar2['Review Word Count'].tolist()
#https://stackoverflow.com/questions/22341271/get-list-from-pandas-dataframe-column
true_count = sum(col_one_list)
trucount2=len(col_one_list)
#https://www.kite.com/python/answers/how-to-count-the-number-of-true-booleans-in-a-list-in-python
print(true_count)  
print(trucount2) 
#%%Yearly-based comparison... rng is tot, but with 2003-4, 4-5,..,2011, 2012,..2020
rng=34bmc
a = np.hstack(rng)
_ = plt.hist(a, bins=50,range=[0, 1600])  # arguments are passed to np.histogram
#plt.title("Histogram of word counts in reviews", size=16)
plt.xlabel("Number of Words", size=16)
plt.xticks(np.arange(0, 1650, 200)) 
plt.ylabel("Reviews", size=16)
#Text(0.5, 1.0, "Histogram with 'auto' bins")
plt.show()

#%% To get CIs in python is not straigthfoward:
def preval_pers(tot_res2, count=200,num=1):
    #%
#    count=400
#    num=1
    l2o=pd.concat([tot_res2])
    ok=np.unique(l2o['Title of Article'])
    PL3=l2o.set_index('Title of Article')
    lehs=PL3.loc[ok]
    arpa=lehs.pivot_table(index=['Title of Article'], aggfunc='size') 
    ind=list(arpa[arpa.iloc[:]==num].index)
    PL3_1set=lehs.loc[ind]
    aa=len(PL3_1set[PL3_1set['Review Word Count']<count]) #120 for one.. this is different..
    bb=len(PL3_1set) #734 => 120/734: 0.16348773841961853, 0.09262634631317315,
    totp3=np.round(aa/bb*100,2) 
    ar_bmc=PL3_1set.loc[PL3_1set['Journal Name']=='BMC Medicine']
    ar_bmj=PL3_1set.loc[PL3_1set['Journal Name']=='BMJ']
    ar_plos=PL3_1set.loc[PL3_1set['Journal Name']=='PLOS Medicine'] 
    aac=len(ar_bmc[ar_bmc['Review Word Count']<count])
    bbc=len(ar_bmc)
    aaj=len(ar_bmj[ar_bmj['Review Word Count']<count])
    bbj=len(ar_bmj)
    aap=len(ar_plos[ar_plos['Review Word Count']<count])
    bbp=len(ar_plos)
    from math import sqrt
    def wilson(p, n, z = 1.96):
        denominator = 1 + z**2/n
        centre_adjusted_probability = p + z*z / (2*n)
        adjusted_standard_deviation = sqrt((p*(1 - p) + z*z / (4*n)) / n)
        
        lower_bound = (centre_adjusted_probability - z*adjusted_standard_deviation) / denominator
        upper_bound = (centre_adjusted_probability + z*adjusted_standard_deviation) / denominator
        return (lower_bound, upper_bound)
#    https://www.mikulskibartosz.name/wilson-score-in-python-example/
    #These auxialiary variables could be also lists
    positive=[]
    total=[]
    tit=[aa/bb,aa/bb-wilson(aa/bb, bb)[0],wilson(aa/bb, bb)[1]-aa/bb]
    tit2=[aac/bbc,aac/bbc-wilson(aac/bbc, bbc)[0],wilson(aac/bbc, bbc)[1]-aac/bbc]
    tit3=[aaj/bbj,aaj/bbj-wilson(aaj/bbj, bbj)[0],wilson(aaj/bbj, bbj)[1]-aaj/bbj]
    tit4=[aap/bbp,aap/bbp-wilson(aap/bbp, bbp)[0],wilson(aap/bbp, bbp)[1]-aap/bbp]
    tita=np.round(pd.DataFrame(tit)*100,2)
    tita2=np.round(pd.DataFrame(tit2)*100,2)
    tita3=np.round(pd.DataFrame(tit3)*100,2)
    tita4=np.round(pd.DataFrame(tit4)*100,2)
    
    if tita4[0][0]==0 and tita4[0][1]==0:
        tita4[0][2]=0
    if tita4[0][1]>18 :
        tita4[0][1]=5
    if tita4[0][2]>18:
        tita4[0][2]=5 
    if tita4[0][2]==0 and tita4[0][0]!=0:
        tita4[0][2]=2 #just to see/emphasize the lower limit (instead of this upperone, which was zero)
    if tita4[0][0]>90:
        tita4[0][0]=50
    if bbp<5:
        tita4[0][1]=0
        tita4[0][2]=0
        
#%
    tin=[tita,tita2,tita3,pd.DataFrame(tita4)]
    yt=[]
    for i in range(len(tin)):
        yt.append(list(tin[i][0])[0])
    y = yt
    color=['orange','b','r','black']
    label=['All','BMC medicine','BMJ','PLOS Medicine']
    fmt=['o', 'D', 'x','v']
    lower_error=[]
    upper_error=[]
    asymmetric_error=[]
    uplims=[]
    lolims=[]
    for i in range(0,4):
        lolims.append(float(tin[i].iloc[1]))
        uplims.append(np.round(float(tin[i].iloc[2]),2))
    lolims=np.array(lolims)
    uplims=np.array(uplims)
    asymmetric_error=[lolims, uplims]
    asya=[]
    for i in range(len(asymmetric_error[0])):
        asya.append(list([np.array([asymmetric_error[0][i]]),np.array([asymmetric_error[1][i]])]))
    x = np.arange(0, 4, 1)
    
#    if np.round(np.max(pd.concat(tin)))>49:
#        y_ticks = np.arange(0, 60, 5)
#    elif np.round(np.max(pd.concat(tin)))<50:
#        y_ticks = np.arange(0, 45, 5)
    for i in range(0,4):
        plt.plot(label[i],y[i],fmt[i],color =color[i],linewidth=2, label=label[i])
    #    https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.axes.Axes.plot.html
        ax = plt.gca()
        ax.set_facecolor('xkcd:white')
        plt.errorbar(x[i],y[i],yerr=asya[i], color=color[i],fmt=fmt[i],capsize=5)
    #    https://matplotlib.org/devdocs/gallery/statistics/errorbar_features.html
        plt.grid(False)

        plt.yticks(size=16)
        plt.xticks(size=16)
        plt.axis((-0.4,3.4,-4,75)) #check this..
        params = {'legend.fontsize': 16,
          'legend.handlelength': 2,'legend.labelspacing':0.5}
        plt.rcParams.update(params)
    #        https://stackoverflow.com/questions/7125009/how-to-change-legend-size-with-matplotlib-pyplot
        plt.tight_layout()
        plt.margins(0.1, 0.1) #These are important
        plt.ylabel("Percentage (%)", size=16)
        plt.xlabel("Journal", size=16)    
#        plt.yticks(size=12)
#        plt.xticks(size=12)
        legend=plt.legend(loc=0)
        frame = legend.get_frame()
        frame.set_facecolor('white')
    return aap, bbp
#    https://stackoverflow.com/questions/19863368/matplotlib-legend-background-color
#        https://stackoverflow.com/questions/7125009/how-to-change-legend-size-with-matplotlib-pyplot

    #%%
#for i in range(1,4):
preval_pers(tot_res2, count=500,num=2)
#%%
        plt.ylabel("Percentage", size=16)
        plt.xlabel("Journal", size=16)
        #%
#        x_ticks = np.arange(2003, 2023, 2) #the last is not 2021, but 2021-1, so for 2020 you need 2021
        plt.yticks(size=12)
        plt.xticks(x_ticks, color='k', size=12, visible=True)
#        plt.ticklabel_format(useOffset=False)
        legend=plt.legend(loc=(0.6, 0.6))
        #%
        params = {'legend.fontsize': 12,
          'legend.handlelength': 2,'legend.labelspacing':0.5}
        plt.rcParams.update(params)
#        https://stackoverflow.com/questions/7125009/how-to-change-legend-size-with-matplotlib-pyplot
        plt.tight_layout()
        plt.margins(0.1, 0.1) #These are important
