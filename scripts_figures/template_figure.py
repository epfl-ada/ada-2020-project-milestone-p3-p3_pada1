import plotly.express as px
import plotly.tools as pt
import pandas as pd
import chart_studio.tools as tls
import chart_studio.plotly as py

username = 'Arturjssln' # your username
api_key = 'H4XMtrMMVkVIcRDyhuc2' # your api key - go to profile > settings > regenerate key
tls.set_credentials_file(username=username, api_key=api_key)

# Load data
data = pd.read_csv("./snowden.csv",names=["month", "interest"], skiprows=[0,1,2])

# Compute figure
# INSERT YOUR FIGURE HERE


# Get html code for figure
url = py.plot(fig, filename = 'snowden', auto_open=False)
print(tls.get_embed(url))