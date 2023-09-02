import pandas as pd
import numpy as np
import pathlib
import matplotlib.pyplot as plt

# pd print settings
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 32)
pd.set_option('display.width', 0)
pd.set_option('display.precision', 3)

plt.rcParams['font.size'] = '14'

# import data
root_path = (r'D:\School\4B (3B courses)\capstone\Battery Model\SAM Export')
root_path = pathlib.Path(root_path)

# SAM csv File
file = 'results_2SidedRoof_5kW_80kWh.csv'
file_location = root_path / file
df = pd.read_csv(file_location)
Batt_Cap = 150

# create date range
datetime = pd.date_range(start ='01-01-2023 00:00:00',end ='12-31-2023 23:00:00', freq ='1H')

# Creating DataFrames
df['DateTime'] = pd.DataFrame(datetime)
df.set_index('DateTime', inplace=True,drop=False)

# Power Required from Grid
df.plot(y='Electricity to load from grid AC | (kW)')
plt.title('Power Required from Grid [kW]')

# Power Generated vs Power Demand
df.plot(y = ['System power generated | (kW)','Lifetime electricity load | (kW)','Electricity to load from battery AC | (kW)'])


fig, ax = plt.subplots()

x = df.index
y = df['Battery state of charge | (%)']

ax.plot(x,y)

ax.set_xlabel('DateTime')
ax.set_ylabel('Battery State of Charge (%)')
name = file.split('_')[1]
capacity = file.split('_')[3]
capacity = capacity[0:len(capacity) - 4]
title = name + ' - ' + capacity
ax.set_title(title)

# df.plot(y = ['System power generated | (kW)','Lifetime electricity load | (kW)'])

df = df[pd.notnull(df['DateTime'])]
print(df)

# Analysis
demand = np.sum(df['Lifetime electricity load | (kW)'])
print('Annual Building Demand:',round(demand,2),'[kWh]')

PV = np.sum(df['System power generated | (kW)'])
print('Annual Solar PV Generation',round(PV,2),'[kWh]')

df['Delta'] = df['System power generated | (kW)'] - df['Lifetime electricity load | (kW)']
df.plot(y='Delta')
print('Maximum required battery discharge Energy Delta:',round(np.min(df['Delta']),2),'[kW]')
print('Maximum required battery recharge Energy Delta:',round(np.max(df['Delta']),2),'[kW]')
print('average Delta:',round(np.mean(df['Delta']),2),'[kW]')

grid = np.sum(df['Electricity to load from grid AC | (kW)'])
print('Annual Energy From the Grid:', round(grid,2),'[kWh]')

df['SOC_delta'] = df['Battery state of charge | (%)'].diff()
SOC_delta_max = np.min(df['SOC_delta'])
print('Maximum Battery Discharge:',round(SOC_delta_max,2),'[%]')
print('Maximum Battery Discharge:',round(SOC_delta_max*Batt_Cap,2),'[kW]')

df.plot(y='SOC_delta')

# Generation from PV + Battery Compared to Demand
df['Total Available Production'] = df['Electricity to load from system AC | (kW)'] + df['Electricity to load from battery AC | (kW)']
df.plot(y=['Lifetime electricity load | (kW)','Total Available Production'],alpha=0.5)
plt.title('Generation from PV + Battery Compared to Demand')
# investigate when power is required from the grid

df = df[df['Electricity to load from grid AC | (kW)']>0]
# print(df)
# print(len(df))

plt.show()
