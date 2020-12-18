import plotly.tools as pt
import pandas as pd
import chart_studio.tools as tls
import chart_studio.plotly as py
import plotly.graph_objects as go

username = "Arturjssln"
api_key = "H4XMtrMMVkVIcRDyhuc2"
tls.set_credentials_file(username=username, api_key=api_key)

fig = go.Figure()
fig.add_trace(go.Bar(x=[0, 1], y=[mean_pre_june, mean_post_june], name="Average interest", width=0.8))
fig.update_traces(marker_color='#1f78b4')

fig.update_layout(template='plotly_white')
fig.update_layout(title='Figure 2: Terrorism-related articles average interest', xaxis=dict(tickmode='array', tickvals=[0,1],ticktext=['Pre June, 2013', 'Post June, 2013']))
fig.update_yaxes(title_text='Average interest', range=[0,100])
fig.update_xaxes(range=[-1,2])


# Get html code for figure
url = py.plot(fig, filename = 'fig2', auto_open=True)
print(tls.get_embed(url))

EVENT_DATE = pd.to_datetime('2013-06-15')

fig = go.Figure()
terrorism_marged_ts = pd.concat([terrorism_pre_june_ts, terrorism_post_june_ts], axis=0)
fig.add_trace(go.Scatter(x=terrorism_marged_ts.date, y=terrorism_marged_ts.max_ratio, name = 'Total interest (Terrorism)', mode='markers', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_pre_june_ts.date, y=intercept_pre_june + slope_pre_june*x1, name = 'Terrorism-related Trend Pre-June 2013', mode='lines', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_post_june_ts.date, y=intercept_post_june + slope_post_june*x2, name = 'Terrorism-related Trend Post-June 2013', mode='lines', line = dict(color = '#a6cee3', width = 4)))

fig.update_layout(template='plotly_white')
fig.update_layout(title='Figure 3: terrorism-related articles interest trends')
fig.update_xaxes(title_text='Time', tickangle=-45)
fig.update_yaxes(title_text='Total interest by week', range=[0, 150])
fig.add_vline(x=EVENT_DATE, line = dict(color = 'black', width = 4))
fig.add_annotation(x=EVENT_DATE, y=130,
            text="Mid-June 2013",
            showarrow=True,
            arrowhead=4,
            arrowwidth=2,
            ax=100)
fig.update_layout(legend = dict(x = 0.0, y = 0.0))
url = py.plot(fig, filename = 'fig3', auto_open=True)

print(url)
print(tls.get_embed(url))


fig = go.Figure()
terrorism_marged_ts = pd.concat([terrorism_pre_june_ts, terrorism_post_june_ts], axis=0)
fig.add_trace(go.Scatter(x=terrorism_marged_ts.date, y=terrorism_marged_ts.max_ratio, name = 'Total interest (Terrorism)', mode='markers', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_pre_june_ts.date, y=intercept_pre_june + slope_pre_june*x1, name = 'Terrorism-related Trend Pre-June 2013', mode='lines', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_post_june_ts.date, y=intercept_post_june + slope_post_june*x2, name = 'Terrorism-related Trend Post-June 2013', mode='lines', line = dict(color = '#a6cee3', width = 4)))

slope_pre_june_dom, intercept_pre_june_dom, _, _, _ = stats.linregress(domestic_pre_june_ts.index, 
                                                               domestic_pre_june_ts.max_ratio)
slope_post_june_dom, intercept_post_june_dom, _, _, _ = stats.linregress(domestic_post_june_ts.index,
                                                                 domestic_post_june_ts.max_ratio)

domestic_marged_ts = pd.concat([domestic_pre_june_ts, domestic_post_june_ts], axis=0)
fig.add_trace(go.Scatter(x=domestic_marged_ts.date, y=domestic_marged_ts.max_ratio, name = 'Total interest (Security)', mode='markers', line = dict(color = '#33a02c', width = 4)))
fig.add_trace(go.Scatter(x=domestic_pre_june_ts.date, y=intercept_pre_june_dom + slope_pre_june_dom*x1, name = 'Security-related Trend Pre-June 2013', mode='lines', line = dict(color = '#33a02c', width = 4)))

fig.add_trace(go.Scatter(x=domestic_post_june_ts.date, y=intercept_post_june_dom + slope_post_june_dom*x2, name = 'Security-related Trend Post-June 2013', mode='lines', line = dict(color = '#78c879', width = 4)))

fig.update_layout(template='plotly_white')
fig.update_layout(title='Figure 4: terrorism- and security-related articles interest trends')
fig.update_xaxes(title_text='Time', tickangle=-45)
fig.update_yaxes(title_text='Total interest by week', range=[0, 150])
fig.add_vline(x=EVENT_DATE, line = dict(color = 'black', width = 4))
fig.add_annotation(x=EVENT_DATE, y=130,
            text="Mid-June 2013",
            showarrow=True,
            arrowhead=4,
            arrowwidth=2,
            ax=100)
fig.update_layout(legend = dict(x = 0.0, y = 0.0))

url = py.plot(fig, filename = 'fig4', auto_open=True)

print(url)
print(tls.get_embed(url))


# TODO: put clean data here
terrorism_pre_june_ts = terrorism30_pre_june_ts
terrorism_post_june_ts = terrorism30_post_june_ts
domestic_pre_june_ts = domestic_pre_june_ts
domestic_post_june_ts = domestic_post_june_ts

slope_pre_june, intercept_pre_june, _, _, _ = stats.linregress(terrorism_pre_june_ts.index, 
                                                               terrorism_pre_june_ts.max_ratio)
slope_post_june, intercept_post_june, _, _, _ = stats.linregress(terrorism_post_june_ts.index,
                                                                 terrorism_post_june_ts.max_ratio)


fig = go.Figure()
terrorism_marged_ts = pd.concat([terrorism_pre_june_ts, terrorism_post_june_ts], axis=0)
fig.add_trace(go.Scatter(x=terrorism_marged_ts.date, y=terrorism_marged_ts.max_ratio, name = 'Total interest (Terrorism)', mode='markers', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_pre_june_ts.date, y=intercept_pre_june + slope_pre_june*x1, name = 'Terrorism-related Trend Pre-June 2013', mode='lines', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_post_june_ts.date, y=intercept_post_june + slope_post_june*x2, name = 'Terrorism-related Trend Post-June 2013', mode='lines', line = dict(color = '#a6cee3', width = 4)))

slope_pre_june_dom, intercept_pre_june_dom, _, _, _ = stats.linregress(domestic_pre_june_ts.index, domestic_pre_june_ts.max_ratio)
slope_post_june_dom, intercept_post_june_dom, _, _, _ = stats.linregress(domestic_post_june_ts.index, domestic_post_june_ts.max_ratio)

domestic_marged_ts = pd.concat([domestic_pre_june_ts, domestic_post_june_ts], axis=0)
fig.add_trace(go.Scatter(x=domestic_marged_ts.date, y=domestic_marged_ts.max_ratio, name = 'Total interest (Security)', mode='markers', line = dict(color = '#33a02c', width = 4)))
fig.add_trace(go.Scatter(x=domestic_pre_june_ts.date, y=intercept_pre_june_dom + slope_pre_june_dom*x1, name = 'Security-related Trend Pre-June 2013', mode='lines', line = dict(color = '#33a02c', width = 4)))
fig.add_trace(go.Scatter(x=domestic_post_june_ts.date, y=intercept_post_june_dom + slope_post_june_dom*x2, name = 'Security-related Trend Post-June 2013', mode='lines', line = dict(color = '#78c879', width = 4)))

fig.update_layout(template='plotly_white')
fig.update_layout(title='Figure 5: terrorism- and security-related articles interest trends')
fig.update_xaxes(title_text='Time', tickangle=-45)
fig.update_yaxes(title_text='Total interest by monweekth', range=[0, 150])
fig.add_vline(x=EVENT_DATE, line = dict(color = 'black', width = 4))
fig.add_annotation(x=EVENT_DATE, y=130,
            text="Mid-June 2013",
            showarrow=True,
            arrowhead=4,
            arrowwidth=2,
            ax=100)
fig.update_layout(legend = dict(x = 0.0, y = 0.0))
            
url = py.plot(fig, filename = 'fig5', auto_open=True)
print(url)
print(tls.get_embed(url))