import pandas as pd
import numpy as np
import pathlib
import matplotlib.pyplot as plt
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

# create Import Installement Cost

capex = 184222
interconnection = 0

file = 'results_2SidedRoof+Overhang_5kW_60kWh.csv'
file_location = root_path / file
df = pd.read_csv(file_location)

# create date range
datetime = pd.date_range(start='01-01-2023 00:00:00', end='12-31-2050 23:00:00', freq='1H')
# Creating DataFrames
df['DateTime'] = pd.DataFrame(datetime)
df.set_index('DateTime', inplace=True, drop=False)
df = df[pd.notnull(df['DateTime'])]

# calculate values and append to list
grid = np.sum(df['Electricity to load from grid AC | (kW)'])

# calculate curtailment
df['Curtailment'] = np.where(df['System power generated | (kW)'] > df['Electricity to load from system AC | (kW)'],
                             df['System power generated | (kW)'] - df['Electricity to load from system AC | (kW)'],
                             0
)

# calculate energy sold
cost_sell_trf = 0.17 # [USD/kWh] - tariff
cost_sell_dg = 0.38 # [USD/kWh] - diesel generator
cost_buy = 0.079 #
df['Excess Energy Sold [USD]'] = df['Curtailment'] * cost_sell_trf
df['Energy required from Grid [USD]'] = df['Electricity to load from grid AC | (kW)'] * cost_buy
df['avoided diesel'] = df['Lifetime electricity load | (kW)'] * cost_sell_dg
df['Cost'] = df['Excess Energy Sold [USD]'] + df['avoided diesel'] - df['Energy required from Grid [USD]']

# resample as annual data
df_annual = df.resample('Y').sum()
df_annual['Year'] = df_annual.index.year

df_annual['Cost'] = np.where(df_annual['Year']==2023,df_annual['Cost']-capex-interconnection,df_annual['Cost'])

print(df_annual)

# print(df)

# calculate NPV

NPV = npf.npv(0.06,df_annual['Cost'])

print('Net Present Value',round(NPV,2),'[$]')


# df_export.to_csv(r'D:\School\4B (3B courses)\capstone\Battery Model\SAM Battery Sensitivity Export.csv')