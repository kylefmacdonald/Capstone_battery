import pandas as pd
import numpy as np
import pathlib
import matplotlib.pyplot as plt
# import pyomo.environ as pyo
# from pyomo.opt import SolverFactory

# create function to optimize state of charge of battery (minimize curtailment and minimize time when power is insufficient for building)
# def dispatch_model_optimization(P, E, Emin, C_i, C_f, n_re, n_dis, data):
#     N = len(data)                               # number of hours in a year
#     # Create the model
#     m = pyo.ConcreteModel()
#
#     # Define a range for the timesteps (based on the numbers of hours in the day)
#     m.TimeSteps = range(N)
#
#     # max we can recharge and discharge is 1 mw per hour, cannot have negative values
#     m.Pc = pyo.Var(m.TimeSteps, domain=pyo.NonNegativeReals, bounds=(0, P))
#     m.Pd = pyo.Var(m.TimeSteps, domain=pyo.NonNegativeReals, bounds=(0, P))
#     # Charge must be between 10% - 100% capacity
#     m.XB = pyo.Var(m.TimeSteps, domain=pyo.NonNegativeReals, bounds=(Emin, E))
#
#     # ----- Set up objective model ----- #
#     #  maximization - Cost is equal to amount we sell (discharge) * price minus amount we buy (recharge) * price
#     m.obj = pyo.Objective(expr=sum(m.Pc[i] * d[i] - m.Pd[i] * d[i] for i in m.TimeSteps))
#
#     # ----- Set up variable constraints ----- #
#
#
#     SOC = 2
#     return SOC

# SOC = []
# def battery_dispatch(Load,Curtailment,P_max,E_max,Boundary):
#     for i in range(len(Load)):
#         if i == 0:
#             SOC = SOC + [Boundary]
#         else:
#             if
#     return SOC

# pd print settings
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 32)
pd.set_option('display.width', 0)
pd.set_option('display.precision', 3)

plt.rcParams['font.size'] = '14'

# import data
root_path = (r'D:\School\4B (3B courses)\capstone\energy demand')
root_path = pathlib.Path(root_path)

# demand file
file = 'EnergyDemand8760_Updated_SAM_Import.csv'
file_location = root_path / file
df_demand = pd.read_csv(file_location)
df_demand['Datetime'] = pd.to_datetime(df_demand['Hourly'])
df_demand['Datetime'] = df_demand['Datetime'].mask(df_demand['Datetime'].dt.year == 2006,df_demand['Datetime'] + pd.offsets.DateOffset(year=1990) + pd.DateOffset(hours=-1))
df_demand['Datetime'] = df_demand['Datetime'].mask(df_demand['Datetime'].dt.year == 2007,df_demand['Datetime'] + pd.offsets.DateOffset(year=1991) + pd.DateOffset(hours=-1))
df_demand.set_index('Datetime', inplace=True, drop=True)
df_demand.index.shift(-1, freq='H')
print(df_demand)
# df_demand.index.shift(-16,freq='Y')
df = df_demand

df['Electricity: Facility (kWh)'] = df['Electricity:Facility kWh']

# # solar pv production file
# file = 'Capstone - 2_sided_Energy_8760.CSV'
# file_location = root_path / file
# df_production = pd.read_csv(file_location,index_col=0, parse_dates={'datetime': [0]})

# print(df_production)
# print(df_demand)

# # concatenate data
# df = pd.concat([df_demand['Electricity kWh'],df_production['EOutInv KW']],axis=1)
# df['Energy Delta'] = df['Electricity kWh'] - df['EOutInv KW']

# calculate average 1 day and 3 day energy demand of the house (repeat for season with higher demand!)
max_power = np.max(df['Electricity: Facility (kWh)'])
print('The max power demand is:',round(max_power,2), '[kW]')
daily_avg = np.mean(df['Electricity: Facility (kWh)'].resample('D').sum())
daily_max = np.max(df['Electricity: Facility (kWh)'].resample('D').sum())
print('The average daily demand of the building is:',round(daily_avg,2),'[kWh]')
print('The maximum daily demand of the building is:',round(daily_max,2),'[kWh]')
print('The average 3 day demand of the building is:',round(daily_avg*3,2),'[kWh]')

# filter for demand at night

df['Hour'] = df.index.hour
df = df[(df['Hour']<=7) | (df['Hour']>=20)]
print(df)
print('Nightime Power Consumption: ',round(np.sum(df['Electricity: Facility (kWh)']),2),'(kWh)')

# # calculate curtailment and times when supply fails to meet demand
# df['EOutInv KW'] = np.where(df['EOutInv KW']==0.001,0,df['EOutInv KW'])
# df['Load adjusted by supply'] = np.where(df['EOutInv KW']>=df['Electricity kWh'],0,df['Electricity kWh']-df['EOutInv KW'])
# df['Curtailment'] = np.where(df['EOutInv KW']>=df['Electricity kWh'],df['EOutInv KW'] - df['Electricity kWh'],0)
#
# # define battery parameters
# battery_lst = ['battery 1']
#
# P = 1                       # Battery Power Capacity [MW] - max we can recharge and discharge is 1 mw per hour
#
# E = 250                       # Battery Energy Capacity [MWh]
# Emin = 0.1 * E
#
# charge_min = 0.1 * E        # Minimum battery capacity [MWh]
#
# C_i = 0.5 * E               # inital state of charge (50%) [MWh] (boundary Condition)
# C_f = 0.5 * E               # final state of charge (50%) [MWh] (boundary Condition)
#
# n_re = 1                    # recharge efficiency [-]
# n_dis = 1                   # discharge efficiency [-]
#
# # calculate battery state of charge
# # df['Battery State of Charge [kWh]'] = C_i
# # df['Battery State of Charge [kWh]'] = np.where(df['Curtailment'] >= 0,
# #                                                np.where(df['Curtailment'] > P,
# #                                                         np.where()
# #                                                    df['Battery State of Charge [kWh]'].shift(periods=-1)+ P
# #                                                         )
# # )
#
#
# # # units below in kW and kWh
# # battery = {
# #     'battery 1':{'Power Limit':12,'Energy Capacity':12}
# # }
#
#
# print(df)
#
# # plot data
# df.plot(y=['Electricity kWh','EOutInv KW'])
# df.plot(y='Energy Delta')
# df.plot(y='Load adjusted by supply')
# df.plot(y='Curtailment')
# plt.show()

