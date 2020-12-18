import plotly.express as px
import plotly.tools as pt
import pandas as pd
import chart_studio.tools as tls
import chart_studio.plotly as py
import plotly.graph_objects as go

username = 'Arturjssln' # your username
api_key = 'H4XMtrMMVkVIcRDyhuc2' # your api key - go to profile > settings > regenerate key
tls.set_credentials_file(username=username, api_key=api_key)

# Load data
data = pd.read_csv("./snowden.csv",names=["month", "interest"], skiprows=[0,1,2])


fig = go.Figure()
#fig.add_trace(go.Scatter(x=..., y=..., name = 'Total views', mode='markers', line = dict(color = '#33a02c', width = 4)))
#fig.add_trace(go.Scatter(x==..., y==..., name = 'Trend Pre-June 2013', mode='lines', line = dict(color = '#33a02c', width = 4)))
#fig.add_trace(go.Scatter(x==..., y==..., name = 'Trend Post-June 2013', mode='lines', line = dict(color = '#78c679', width = 4)))
fig.update_layout(template='plotly_white')
fig.update_layout(title='Pre and Post June 2013 terrorism-related articles views trends')
fig.update_xaxes(title_text='Time', tickangle=-45)
fig.update_yaxes(title_text='Total views by month', range=[0, 1.5e6])



# Get html code for figure
url = py.plot(fig, filename = 'test', auto_open=False)
print(tls.get_embed(url))