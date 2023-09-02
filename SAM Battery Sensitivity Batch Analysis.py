import pandas as pd
import numpy as np
import pathlib
import matplotlib.pyplot as plt
import os
import numpy_financial as npf

# pd print settings
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 32)
pd.set_option('display.width', 0)
pd.set_option('display.precision', 3)

plt.rcParams['font.size'] = '14'

# import data
root_path = (r'D:\School\4B (3B courses)\capstone\Battery Model\SAM Export')
root_path = pathlib.Path(root_path)

# import Data
files = os.listdir(root_path)
print(files)
curt_ls = []
grid_ls = []
system_id_ls = []
battery_capacity_ls = []
profit_ls = []
NPV_ls = []
LCOE_ls = []
PV_yeild = []
curtailment = []
discount_rate_ls = []
IRR_ls = []

# Import Installment Cost
df_capex = pd.read_csv(r'D:\School\4B (3B courses)\capstone\Battery Model\Capex.csv')

discount_rate = [0.01,0.02,0.03,0.04,0.05,0.06]

for i in range(len(files)):
    file = files[i]
    file_location = root_path / file
    df = pd.read_csv(file_location)
    # create date range
    datetime = pd.date_range(start='01-01-2023 00:00:00', end='12-31-2050 23:00:00', freq='1H')
    # Creating DataFrames
    df['DateTime'] = pd.DataFrame(datetime)
    df.set_index('DateTime', inplace=True, drop=False)
    df = df[pd.notnull(df['DateTime'])]
    project_life = np.max(df.index.year) - np.min(df.index.year)

    # calculate values and append to list
    grid = np.sum(df['Electricity to load from grid AC | (kW)'])/project_life

    name = file.split('_')[1]
    capacity = file.split('_')[3]
    capacity = capacity[0:len(capacity)-7]

    # calculate curtailment
    df['Curtailment'] = np.where(df['System power generated | (kW)'] > df['Electricity to load from system AC | (kW)'],
                                 df['System power generated | (kW)'] - df['Electricity to load from system AC | (kW)'],
                                 0
    )

    annual_curtailment = np.sum(df['Curtailment']) / project_life
    # calculate energy sold
    cost_sell = 0.22125 # [USD/kWh]
    cost_buy = 0.079 # [USD/kWh]
    df['Energy Sold [USD]'] = df['Curtailment'] * cost_sell
    df['Energy Buy'] = df['Electricity to load from grid AC | (kW)'] * cost_buy
    annual_profit = np.sum(df['Energy Sold [USD]'])

    # create annual df
    fuel = 9000 # $/yr
    diesel_capex = 10000 # $
    building
    capex = df_capex[(df_capex['PV System'] == str(name)) & (df_capex['Battery Capacity'] == int(capacity))]
    capex = capex['Installed Cost'].values[0]
    df_annual = df.resample('Y').sum()
    df_annual['Year'] = df_annual.index.year
    df_annual['Cash Flow'] = np.where(df_annual['Year'] == 2023,df_annual['Energy Sold [USD]'] - capex + diesel_capex + fuel-df_annual['Energy Buy'],df_annual['Energy Sold [USD]']+fuel-df_annual['Energy Buy'])
    for j in range(len(discount_rate)):
        rate = discount_rate[j]
        discount_rate_ls = discount_rate_ls + [rate]
        NPV = npf.npv(rate,df_annual['Cash Flow'])
        LCOE = npf.npv(rate,df_annual['Cash Flow']/df_annual['System power generated | (kW)'])
        IRR = npf.irr(df_annual['Cash Flow'])
        NPV_ls = NPV_ls + [NPV]
        LCOE_ls = LCOE_ls + [LCOE]
        grid_ls = grid_ls + [grid]
        system_id_ls = system_id_ls + [name]
        battery_capacity_ls = battery_capacity_ls + [capacity]
        curt_ls = curt_ls + [annual_curtailment]
        profit_ls = profit_ls + [annual_profit]
        IRR_ls = IRR_ls + [IRR]
        text = name + ' ' + capacity
    if name == 'SouthRoof+Overhang':
        df_annual.to_csv('SouthRoof+Overhang Annual.csv')
        if i == np.max(len(discount_rate)-1):
            plt.plot(discount_rate_ls,NPV_ls,label = text)
    # df_annual.to_csv(r'D:\School\4B (3B courses)\capstone\Battery Model\SAM Battery Sensitivity Export.csv')

    # print(df)
plt.show()
df_export = pd.DataFrame({'System': system_id_ls,
     'Battery Capacity': battery_capacity_ls,
     'Energy Required from Grid': grid_ls,
     'Annual Curtailment':curt_ls,
     'Annual Profit':profit_ls,
     'Net Present Value': NPV_ls,
     'LCOE':LCOE_ls,
     'IRR':IRR_ls,
     'Discount Rate':discount_rate_ls
    })

print(df_export)

df_export.to_csv(r'D:\School\4B (3B courses)\capstone\Battery Model\SAM Battery Sensitivity Export.csv')