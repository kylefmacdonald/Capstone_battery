import pandas as pd
import numpy as np
import pathlib
import matplotlib.pyplot as plt
import os
import numpy_financial as npf
import plotly.express as px

# pd print settings
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 32)
pd.set_option('display.width', 0)
pd.set_option('display.precision', 3)

plt.rcParams['font.size'] = '26'

# import data
root_path = (r'D:\School\4B (3B courses)\capstone\Battery Model')
root_path = pathlib.Path(root_path)

file = 'results_SouthRoof+Overhang_5kW_60kWh.csv'

location = root_path / 'SAM Export' / file

df = pd.read_csv(location)

location = root_path / 'climate' / '444745_7.37_3.90_2019.csv'

df_climate = pd.read_csv(location)
df_climate['Year'] = 2023
df_climate['DateTime'] = pd.to_datetime(dict(year=df_climate.Year, month=df_climate.Month, day=df_climate.Day))
df_climate.set_index('DateTime', inplace=True, drop=False)
print(df_climate)
temp_daily = df_climate['Temperature'].resample('D').mean()
GHI_daily = df_climate['GHI'].resample('D').mean()

datetime = pd.date_range(start='01-01-2023 00:00:00', end='12-31-2050 23:00:00', freq='1H')
# Creating DataFrames
df['DateTime'] = pd.DataFrame(datetime)
df.set_index('DateTime', inplace=True, drop=False)
df = df[pd.notnull(df['DateTime'])]
df['Year'] = df.index.year
project_life = np.max(df.index.year) - np.min(df.index.year)
df = df[df['Year'] == 2023]

annual_yield = np.sum(df['System power generated | (kW)'])
print('Annual Yield:',annual_yield)

df['Curtailment'] = np.where(df['System power generated | (kW)'] > df['Electricity to load from system AC | (kW)'],
                             df['System power generated | (kW)'] - df['Electricity to load from system AC | (kW)'],
                             0
                             )
df['Curtailment2'] = df['System power generated | (kW)'] - df['Electricity to load from system AC | (kW)'] + df['Lifetime electricity load | (kW)']

df_daily = df.resample('W').sum()
df_daily['Day'] = df_daily.index.day
df_daily['Temp'] = temp_daily
df_daily['GHI'] = GHI_daily
print(df_daily)

# fig, axes = plt.subplots(3, 1,sharex='col')
# df_daily.plot(y = 'Lifetime electricity load | (kW)',ax=axes[0],label = 'Energy Demand',color = 'cornflowerblue')
# axes[0].fill_between(df_daily.index,df_daily['Lifetime electricity load | (kW)'],alpha=0.3)
# df_daily.plot(y = 'Electricity to load from system AC | (kW)',ax=axes[1],label = 'Energy Supplied By Solar PV System',color = 'gold')
# df_daily.plot(y = 'Electricity to load from battery AC | (kW)',ax=axes[1],label = 'Energy Supplied By Battery',color = 'firebrick')
# df_daily.plot(y = 'Curtailment',ax=axes[2],label = 'Excess Energy Produced',color = 'forestgreen')
# axes[0].get_legend().remove()
# axes[1].get_legend().remove()
# axes[2].get_legend().remove()
#
# fig.supylabel('Energy [kWh]')
#
# fig.legend(loc="center right")
#
# # Adjusting the sub-plots
# plt.subplots_adjust(right=0.75)
#
# plt.show()

# new plot


fig, axes = plt.subplots()
df_daily.plot(y = 'Lifetime electricity load | (kW)',ax=axes,label = 'Energy Demand',color = 'darkgreen',linewidth=0.8)
df_daily.plot(y = 'Electricity to load from system AC | (kW)',ax=axes,label = 'Energy Supplied By Solar PV System',color = 'maroon',linewidth=1,alpha=0.6)
axes.fill_between(df_daily.index,df_daily['Lifetime electricity load | (kW)'],df_daily['Electricity to load from system AC | (kW)'],color = 'maroon',alpha=0.5,label='Energy Supply')

df_daily.plot(y = 'Curtailment2',ax=axes,label = 'Excess Energy Produced',color = 'seagreen',linewidth=1,alpha =1 )
axes.fill_between(df_daily.index,df_daily['Lifetime electricity load | (kW)'],df_daily['Curtailment2'],color = 'seagreen',alpha=0.7,label = 'Excess Energy Sold to the Grid')
plt.ylabel('Energy [kWh]')
plt.title('Weekly Energy Profile')

axes.get_legend().remove()


# fig.legend(loc="center right")
#
# # Adjusting the sub-plots
# plt.subplots_adjust(right=0.75)

plt.show()

fig, axes = plt.subplots(2, 1,sharex='col')
# df_daily.plot(y = 'Lifetime electricity load | (kW)',ax=axes[0],label = 'Energy Demand',color = 'cornflowerblue',linewidth=1)
# df_daily.plot(y = 'Electricity to load from system AC | (kW)',ax=axes[0],label = 'Energy Supplied By Solar PV System',color = 'gold',linewidth=1)
# axes[0].fill_between(df_daily.index,df_daily['Lifetime electricity load | (kW)'],df_daily['Electricity to load from system AC | (kW)'],color = 'firebrick',alpha=0.7)

# df_daily.plot(y = 'Curtailment',ax=axes[0],label = 'Excess Energy Produced',color = 'forestgreen',linewidth=1)
# axes[0].fill_between(df_daily.index,df_daily['Lifetime electricity load | (kW)'],df_daily['Curtailment'],color = 'forestgreen',alpha=0.7)

df_daily.plot(y = 'Electricity to load from battery AC | (kW)',ax=axes[0],label = 'Energy Supplied By Battery',color = 'firebrick',linewidth=1)
axes[0].fill_between(df_daily.index,df_daily['Electricity to load from battery AC | (kW)'],color = 'firebrick',alpha=0.7)

df_daily.plot(y = 'Curtailment',ax=axes[1],label = 'Excess Energy Produced',color = 'forestgreen',linewidth=1)
axes[1].fill_between(df_daily.index,df_daily['Curtailment'],color = 'forestgreen',alpha=0.7)

axes[0].get_legend().remove()
axes[1].get_legend().remove()
# axes[2].get_legend().remove()

fig.supylabel('Energy [kWh]')

fig.legend(loc="center right")

# Adjusting the sub-plots
plt.subplots_adjust(right=0.75)

plt.show()


