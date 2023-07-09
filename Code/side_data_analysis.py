import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import prepare_df
from xyplot_core import *
#import side_data_analysis

def plot_particular_option(pdata,strike,cpflag):
    
    #plot particular call option 1500, maturity less than 100 days for example
    
    strike975=pdata['strike']==strike
    iscall=pdata['cpflag']==cpflag
    
    shortmaturity1=pdata['maturity']<150
    shortmaturity2=pdata['maturity']<120
    shortmaturity3=pdata['maturity']<90
    shortmaturity4=pdata['maturity']<60
    shortmaturity5=pdata['maturity']<30
    
    ss1=pdata[strike975 & iscall & shortmaturity1]
    ss2=pdata[strike975 & iscall & shortmaturity2]
    ss3=pdata[strike975 & iscall & shortmaturity3]
    ss4=pdata[strike975 & iscall & shortmaturity4]
    ss5=pdata[strike975 & iscall & shortmaturity5]
        
   
    if cpflag=="C":
        name="Call option price distribution (X="+str(strike)+")"
    else:
        name="Put option price distribution (X="+str(strike)+")"
    
    plot1=my_plot()
    plot1.append_data(ss2['close'],ss2['mid'], 'k', '90<T<120',linewidth=1.5)
    plot1.append_data(ss3['close'],ss3['mid'], 'r', '60<T<90',linewidth=1.5)
    plot1.append_data(ss4['close'],ss4['mid'], 'b', '30<T<60',linewidth=1.5)
    plot1.append_data(ss5['close'],ss5['mid'], 'g', 'T<30',linewidth=1.5)
    plot1.construct_plot(name,"$S$","$"+cpflag+"$",save=str(cpflag)+str(strike)+".png",xymin=[1050,0],xymax=[1550,200],scatter=True)
   
  
def plot_particular_option(pdata,strike,cpflag):
    
    #plot particular call option 1500, maturity less than 100 days for example
    
    strike975=pdata['strike']==strike
    iscall=pdata['cpflag']==cpflag
    
    shortmaturity1=pdata['maturity']<150
    shortmaturity2=pdata['maturity']<120
    shortmaturity3=pdata['maturity']<90
    shortmaturity4=pdata['maturity']<60
    shortmaturity5=pdata['maturity']<30
    
    ss1=pdata[strike975 & iscall & shortmaturity1]
    ss2=pdata[strike975 & iscall & shortmaturity2]
    ss3=pdata[strike975 & iscall & shortmaturity3]
    ss4=pdata[strike975 & iscall & shortmaturity4]
    ss5=pdata[strike975 & iscall & shortmaturity5]
        
   
    if cpflag=="C":
        name="Call option price distribution (X="+str(strike)+")"
    else:
        name="Put option price distribution (X="+str(strike)+")"
    
    plot1=my_plot()
    plot1.append_data(ss2['close'],ss2['mid'], 'k', '90<T<120',linewidth=1.5)
    plot1.append_data(ss3['close'],ss3['mid'], 'r', '60<T<90',linewidth=1.5)
    plot1.append_data(ss4['close'],ss4['mid'], 'b', '30<T<60',linewidth=1.5)
    plot1.append_data(ss5['close'],ss5['mid'], 'g', 'T<30',linewidth=1.5)
    plot1.construct_plot(name,"$S$","$"+cpflag+"$",save=str(cpflag)+str(strike)+".png",xymin=[1050,0],xymax=[1550,200],scatter=True)

def plot_particular_moneyness(pdata,cpflag):
    
    #plot particular call option 1500, maturity less than 100 days for example
    
    moneyness1=pdata['moneyness']<0.97
    moneyness2=pdata['moneyness']>0.97
    moneyness2b=pdata['moneyness']<=1.05
    moneyness3=pdata['moneyness']>1.05
    iscall=pdata['cpflag']==cpflag
    
    shortmaturity1=pdata['maturity']>=180
    shortmaturity2=pdata['maturity']<180
    shortmaturity3=pdata['maturity']<60
    

    ss1=pdata[moneyness1 & iscall & shortmaturity1]
    ss2=pdata[moneyness1 & iscall & shortmaturity2]
    ss3=pdata[moneyness1 & iscall & shortmaturity3]

    ss4=pdata[moneyness2 & moneyness2b & iscall & shortmaturity1]
    ss5=pdata[moneyness2 & moneyness2b & iscall & shortmaturity2]
    ss6=pdata[moneyness2 & moneyness2b & iscall & shortmaturity3]
        
    ss7=pdata[moneyness3 & iscall & shortmaturity1]
    ss8=pdata[moneyness3 & iscall & shortmaturity2]
    ss9=pdata[moneyness3 & iscall & shortmaturity3]
        

        
   
    if cpflag=="C":
        name="Call option moneyness distribution"
    else:
        name="Put option moneyness distribution"
    
    
    plot1=my_plot()
    plot1.append_data(ss1['moneyness'],ss1['mid_strike'], '#550099', '$T\geq180$',linewidth=1.0)
    plot1.append_data(ss2['moneyness'],ss2['mid_strike'], '#000099', '$180>T\geq60$',linewidth=1.0)
    plot1.append_data(ss3['moneyness'],ss3['mid_strike'], '#009999', '$60>T$',linewidth=1.0)
    
    plot1.append_data(ss4['moneyness'],ss4['mid_strike'], '#7700cc', '',linewidth=1.0)
    plot1.append_data(ss5['moneyness'],ss5['mid_strike'], '#0000cc', '',linewidth=1.0)
    plot1.append_data(ss6['moneyness'],ss6['mid_strike'], '#00cccc', '',linewidth=1.0)
    
    plot1.append_data(ss7['moneyness'],ss7['mid_strike'], '#9900ee', '',linewidth=1.0)
    plot1.append_data(ss8['moneyness'],ss8['mid_strike'], '#0000ee', '',linewidth=1.0)
    plot1.append_data(ss9['moneyness'],ss9['mid_strike'], '#00eeee', '',linewidth=1.0)
    
    
    
    
    
    
    vlines=[0.97,1.05]
    plot1.construct_plot(name,"Moneyness $S/X$","$"+cpflag+"/X$",save="Moneyness_"+str(cpflag)+".png",xymin=[0.8,0.0],xymax=[1.3,0.25],scatter=True,vlines=vlines)


def plot_close(underlying):
    
    plot2=my_plot()
    plot2.append_data(underlying['day'],underlying['close'], 'k', 'S&P500 daily closing price',linewidth=1.0)
    plot2.construct_plot("S&P500 daily closing price","Date","S",save="close.png",xticks_bool=True,xymin=[0,1000],xymax=[761,1600],figsize=(10,5))
    
    

def plot_returns(underlying):
    
    plot2=my_plot()
    plot2.append_data(underlying['day'],underlying['returns'], 'k', 'Returns',linewidth=1.0)
    plot2.construct_plot("Returns","Date","Returns",save="returns.png",xticks_bool=True,xymin=[0,-0.025],xymax=[761,0.025],figsize=(10,5))

def plot_volatilities(underlying):
    plot2=my_plot()
    plot2.append_data(underlying['day'],underlying['volatility5'], 'k', '$\sigma_{MA5}$',linewidth=1.0)
    plot2.append_data(underlying['day'],underlying['volatility20'], 'r', '$\sigma_{MA20}$',linewidth=1.5)
    plot2.append_data(underlying['day'],underlying['volatility60'], 'g', '$\sigma_{MA60}$',linewidth=2.0)
    plot2.append_data(underlying['day'],underlying['volatility100'], 'b', '$\sigma_{MA100}$',linewidth=2.5)
    plot2.construct_plot("Volatility","Date","Volatility ($\sigma$)",save="volatility.png",xticks_bool=True,xymin=[0,0],xymax=[761,0.20],figsize=(10,5))
    


def plot_black_scholes_prediction(pdata):
    pdata_plt=pdata[:100000]
    plt.scatter(pdata_plt['mid'],pdata_plt['BS5'])
    plt.scatter(pdata_plt['mid'],pdata_plt['BS20'])
    plt.scatter(pdata_plt['mid'],pdata_plt['BS60'])
    plt.scatter(pdata_plt['mid'],pdata_plt['BS100'])
    plt.show()
    










