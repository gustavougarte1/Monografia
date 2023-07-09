import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import prepare_df
import side_data_analysis
import black_scholes
import modular_nn
import diebold_mariano_test



pdata=prepare_df.prepare_dataframe()



side_data_analysis.plot_particular_option(pdata,1400,"C")
side_data_analysis.plot_particular_option(pdata,1300,"C")
side_data_analysis.plot_particular_option(pdata,1200,"C")
side_data_analysis.plot_particular_option(pdata,1100,"C")

side_data_analysis.plot_particular_option(pdata,1400,"P")
side_data_analysis.plot_particular_option(pdata,1300,"P")
side_data_analysis.plot_particular_option(pdata,1200,"P")
side_data_analysis.plot_particular_option(pdata,1100,"P")
 
#side_data_analysis.plot_particular_moneyness(pdata,"C")
#side_data_analysis.plot_particular_moneyness(pdata,"P")




pdata=prepare_df.add_risk_free_rate_from_FED_to_pdata(pdata)

print(pdata)


underlying=prepare_df.prepare_underlying_asset(pdata)

pdata = prepare_df.append_volatility_columns(pdata,underlying)



side_data_analysis.plot_close(underlying)
side_data_analysis.plot_returns(underlying)
side_data_analysis.plot_volatilities(underlying)


#Takes long time
pdata=black_scholes.compute_and_append_black_scholes_columns(pdata)
pdata=black_scholes.append_moneyness_columns(pdata)


#pdata = pdata_save
pdata_save = pdata


#print(pdata)
side_data_analysis.plot_black_scholes_prediction(pdata)




no_options,no_calls,no_puts,calls,puts,c_tr,c_test,p_tr,p_test = prepare_df.prepare_train_test_set(pdata)

calls_mod,puts_mod = modular_nn.divide_options_to_modules(calls,puts)





def summary_table(calls_mod):
    #Summary table
    #order:  0.97, t1,t2,t3, 1.00 t1,t2,t3, 1.05 t1,t2,t3
    calls_mod_mids=[calls_mod[i]['mid'].mean() for i in range(9)]
    calls_mod_counts=[len(calls_mod[i]) for i in range(9)]
    print(calls_mod_mids,calls_mod_counts)
    
    calls_mod_mids_means=[calls_mod[0+i]['mid'].append(calls_mod[1+i]['mid'], ignore_index=True).append(calls_mod[2+i]['mid'], ignore_index=True).mean() for i in range(0,9,3)]
    print(calls_mod_mids_means)
    
#summary_table(calls_mod)
#summary_table(puts_mod)



def volatility_table(calls_mod):
    #Volatility table
    #order:  0.97, t1,t2,t3, 1.00 t1,t2,t3, 1.05 t1,t2,t3    
    
    calls_mod_implied_vol=[calls_mod[i]['implied'].mean() for i in range(0,9)]
    print("\\% & ".join([str(round(item*100,2)) for item in calls_mod_implied_vol]))
    
    calls_mod_vol5=[calls_mod[i]['volatility5'].mean() for i in range(0,9)]
    print("\\% & ".join([str(round(item*100,2)) for item in calls_mod_vol5]))
    calls_mod_vol20=[calls_mod[i]['volatility20'].mean() for i in range(0,9)]
    print("\\% & ".join([str(round(item*100,2)) for item in calls_mod_vol20]))
    calls_mod_vol60=[calls_mod[i]['volatility60'].mean() for i in range(0,9)]
    print("\\% & ".join([str(round(item*100,2)) for item in calls_mod_vol60]))
    calls_mod_vol100=[calls_mod[i]['volatility100'].mean() for i in range(0,9)]
    print("\\% & ".join([str(round(item*100,2)) for item in calls_mod_vol100]))
    calls_mod_volgarch=[calls_mod[i]['vol_garch'].mean() for i in range(0,9)]
    print("\\% & ".join([str(round(item*100,2)) for item in calls_mod_volgarch]))


    
    calls_mod_vol5_means=[calls_mod[0+i]['volatility5'].append(calls_mod[1+i]['volatility5'], ignore_index=True).append(calls_mod[2+i]['volatility5'], ignore_index=True).mean() for i in range(0,9,3)]
    calls_mod_vol20_means=[calls_mod[0+i]['volatility20'].append(calls_mod[1+i]['volatility20'], ignore_index=True).append(calls_mod[2+i]['volatility20'], ignore_index=True).mean() for i in range(0,9,3)]
    calls_mod_vol60_means=[calls_mod[0+i]['volatility60'].append(calls_mod[1+i]['volatility60'], ignore_index=True).append(calls_mod[2+i]['volatility60'], ignore_index=True).mean() for i in range(0,9,3)]
    calls_mod_vol100_means=[calls_mod[0+i]['volatility100'].append(calls_mod[1+i]['volatility100'], ignore_index=True).append(calls_mod[2+i]['volatility100'], ignore_index=True).mean() for i in range(0,9,3)]
    calls_mod_volgarch_means=[calls_mod[0+i]['vol_garch'].append(calls_mod[1+i]['vol_garch'], ignore_index=True).append(calls_mod[2+i]['vol_garch'], ignore_index=True).mean() for i in range(0,9,3)]
    calls_mod_implied_vol_means=[calls_mod[0+i]['implied'].append(calls_mod[1+i]['implied'], ignore_index=True).append(calls_mod[2+i]['implied'], ignore_index=True).mean() for i in range(0,9,3)]
    print(calls_mod_implied_vol_means,calls_mod_volgarch_means)#calls_mod_vol5_means,calls_mod_vol20_means,calls_mod_vol60_means,calls_mod_vol100_means)

volatility_table(calls_mod)
volatility_table(puts_mod)






"""
##### SIMULATIONS PART

#from collections import Counter
#strikes_count=Counter(list(pdata.strike))
#print(strikes_count,max(strikes_count.keys()))







#calls_mod.append(calls)
#puts_mod.append(puts)
#all_mod = calls_mod+puts_mod
all_mod = [calls,puts]

cpflag="C"
a=0
for module in all_mod:
    a=a+1
    if a==2:
        cpflag="P"
    set_tr,set_test=prepare_df.prepare_train_test_set_module(module)

    #set_tr=c_tr
    #set_test=c_test
    
    
    varlist_vol=['normmat','moneyness','volatility5','volatility20','volatility60','volatility100']
    #varlist_vol=['normmat','moneyness','vol_garch']
    garch=False
    
    X_tr,y_tr,X_test,y_test=modular_nn.load_train_test_set(set_tr,set_test,varlist=varlist_vol)

    
    X_tr_v = np.copy(X_tr)
    y_tr_v = np.copy(y_tr)
    virtual=0
    for number_of_virtual in [0]:#]:
        if number_of_virtual!=0:
            for i in range(len(underlying)):
                if i%100==0:
                    print(i,"/",len(underlying))
                X_tr_v,y_tr_v=modular_nn.virtual_call_option(underlying,X_tr_v,y_tr_v,i,number_of_virtual,cpflag=cpflag,garch=garch)
            print(len(X_tr_v),len(y_tr_v),len(X_tr),len(y_tr_v))    
            virtual = len(y_tr_v)-len(y_tr)
        models=modular_nn.run_neural_network(underlying,X_tr_v,y_tr_v,X_test,y_test,varlist_vol,set_test,virtual)
"""

#bsvirtual_X_tr_save=bsvirtual_X_tr
#bsvirtual_y_tr_save=bsvirtual_y_tr
"""

bsvirtual_X_tr=X_tr[0:0]
bsvirtual_X_test=X_test[0:0]
bsvirtual_y_tr=y_tr[0:0]
bsvirtual_y_test=y_test[0:0]

for i in range(40):
    #if i%100==0:
    print(i)
    bsvirtual_X_tr,bsvirtual_y_tr=modular_nn.bsvirtual_append_lot(bsvirtual_X_tr,bsvirtual_y_tr,underlying)
for i in range(50):
    print(i)
    bsvirtual_X_test,bsvirtual_y_test=modular_nn.bsvirtual_append_lot(bsvirtual_X_test,bsvirtual_y_test,underlying)
"""

"""
writer = pd.ExcelWriter("bsvirtual_X_tr.xlsx")
pd.DataFrame(bsvirtual_X_tr).to_excel(writer,'Sheet1')
writer.save()  
writer = pd.ExcelWriter("bsvirtual_y_tr.xlsx")
pd.DataFrame(bsvirtual_y_tr).to_excel(writer,'Sheet1')
writer.save()  
writer = pd.ExcelWriter("bsvirtual_X_test.xlsx")
pd.DataFrame(bsvirtual_X_test).to_excel(writer,'Sheet1')
writer.save()  
writer = pd.ExcelWriter("bsvirtual_y_test.xlsx")
pd.DataFrame(bsvirtual_y_test).to_excel(writer,'Sheet1')
writer.save()  
"""
"""
nefunguje z nejakeho duvodu
bsvirtual=pd.read_excel("bsvirtual.xlsx")
bsvirtual_X_tr=bsvirtual[['normmat','moneyness','volatility5','volatility20','volatility60','volatility100']]
bsvirtual_y_tr=bsvirtual[['mid_strike']]
bsvirtual_X_test=np.array(bsvirtual_X_tr[300000:])
bsvirtual_y_test=np.array(bsvirtual_y_tr[300000:]).flatten()
bsvirtual_X_tr=np.array(bsvirtual_X_tr[:300000])
bsvirtual_y_tr=np.array(bsvirtual_y_tr[:300000]).flatten()



#print(max(bsvirtual_X_tr[:,1]))
"""


"""
list1=[3]#[3,7,14,29]
for i in list1:#range(30):
    models=modular_nn.run_neural_network(underlying,X_tr[0:(i+1)*10000],bsvirtual_y_tr[0:(i+1)*10000],X_test,bsvirtual_y_test,varlist_vol,c_test)
"""


#print(max(pdata['moneyness']))




