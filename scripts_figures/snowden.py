import plotly.express as px
import plotly.tools as pt
import pandas as pd
import chart_studio.tools as tls
import chart_studio.plotly as py

username = 'Arturjssln' # your username
api_key = 'H4XMtrMMVkVIcRDyhuc2' # your api key - go to profile > settings > regenerate key
tls.set_credentials_file(username=username, api_key=api_key)


data = pd.read_csv("./snowden.csv",names=["month", "interest"], skiprows=[0,1,2])

fig =px.line(x=pd.to_datetime(data.month), y=data.interest)
fig.update_layout(template='plotly_white')
fig.update_layout(title='Snowden interest over time')

url = py.plot(fig, filename = 'snowden', auto_open=False)

print(tls.get_embed(url))