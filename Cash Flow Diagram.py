import pandas as pd
import plotly.express as px
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# pd print settings
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 32)
pd.set_option('display.width', 0)
pd.set_option('display.precision', 3)

# import data
root_path = (r'D:\School\4B (3B courses)\capstone\Battery Model')
root_path = pathlib.Path(root_path)
file = root_path / 'Cash Flow Data.csv'
df = pd.read_csv(file)
print(df)
df['Year'] = df['Year'] + 1

fig = px.bar(df,x = 'Year',y = ['Baseline Annual Costs Savings','Baseline Diesel Capex Saving','Excess Energy Sold',
                                'Diesel Generator OPEX','Solar PV + Battery Capex','Building Upgrade Capex','Solar PV Opex'],
             color_discrete_sequence=['#006400','#008000','#2e8b57','#77dd77','#800000','#b22222','#ff6961'])

fig.update_layout(plot_bgcolor = "white",xaxis_title='Year',yaxis_title='Dispursements and Receipts [$]',
        font=dict(
        family="Calibri",
        size=30)
                  )

fig.show()