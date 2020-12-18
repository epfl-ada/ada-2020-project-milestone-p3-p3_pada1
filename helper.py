import gtab
import requests
import pandas as pd
import sys

def create_search_terms_to_GKG_node_df(search_terms, domain_name, API_key):
    """
    Creates a dataframe mapping a list of search terms to their GKG node representation.
    We make the assumption that the first google result corresponds to the correct topic representation
    (has the highest resultScore).
    This assumption should hold for our project as the terms are not ambuiguous.
    The returned dataframe has attributes:
    {search_term, node_equivalent, domain_name}

    Args:
        search_terms (list[string]): List of all required search queries to map
        domain_name (str): domain of the search queries (ie. terrorims, domestic, top_30_terrorism)
        API_key (str): API key to use for the requests

    Returns:
        dataframe: dataframe mapping search term to their GKG node representation

    """

    # Create function which uses the GKG Api to find the corresponding node for one search query
    def map_search_term(search_term, API_key):
        """
        Maps one search query to the first google result search node representation
        """
        
        # Create base request url
        base_request_prefix = "https://kgsearch.googleapis.com/v1/entities:search"

        # Create parameters for the request
        params = {
            "query" : search_term,
            "key"   : API_key,
            "limit" : 10, # min is 10 but we care only about the first search
            "indent": True
        }
        r = requests.get(base_request_prefix, params = params)
        
        # Find the Google Knowledge Graph Search entity id
        entity_id = r.json()["itemListElement"][0]["result"]['@id'].split(":")[1]
        # Find the Google Knowledge Graph Search entity name
        entity_name = r.json()["itemListElement"][0]["result"]['name']
        
        return (entity_id, entity_name)
    
    # Map search terms to entity id and name equivalent
    entities = [map_search_term(search_term, API_key) for search_term in search_terms]
    
    # Extract entity ids
    entity_ids = [entity[0] for entity in entities]
    
    # Extract entity names
    entity_names = [entity[1] for entity in entities]
    
    # Create domain column
    domain_column = [domain_name]*len(entities)
    
    # Create dictionary for the df
    data={
        "search_term" : search_terms,
        "entity_id"   : entity_ids,
        "entity_name" : entity_names,
        "domain_name" : domain_column
    }
    
    # return the mapping df
    return pd.DataFrame(data=data)

def fix_topics(dataframe, id_replacement, name_replacement, topics_id_to_delete):
    """Fixes topic errors in the dataframe due to ambiguous seach terms, duplicates and non-existing topics.   

    Args:
        dataframe (dataframe): dataframe to fix topic. Requires "entity_name" and "entity_id" columns
        id_replacement (dict): dictionary mapping erronous entity id to correct id
        name_replacement (dict): dictionary mapping erronous entity name to correct name
        topics_to_delete (list(str)): List of all topics ids for which to delete the rows
    Returns:
        dataframe: dataframe with the erronous entries fixed
    """

    # Change required entries and leave the rest
    dataframe["entity_id"] = dataframe["entity_id"] \
                                    .apply(lambda x: id_replacement.get(x) if id_replacement.get(x) is not None else x)
    
    dataframe["entity_name"] = dataframe["entity_name"] \
                                    .apply(lambda x: name_replacement.get(x) if name_replacement.get(x) is not None else x)
    
    # Remove duplicate topics
    dataframe = dataframe.drop_duplicates(subset = ["entity_id", "entity_name"])
    
    # Remove topics that have no corresponding google trends topics
    mask = dataframe["entity_id"].apply(lambda x: x not in topics_id_to_delete)
    
    return dataframe[mask]
 

def create_and_set_gtab(start_timeframe, end_timeframe, geo, gtab_path = "gtab_data"):
    """
    Creates and sets a gtab to the required options.
    This functions takes a lot of time if the anchorbank was not yet created.
    It also creates a directory if needed to the gtab_path

    Args:
    -------
        start_timeframe (str): start of the timeframe for the queries (included)
        end_timeframe (str): end of the timeframe for the queries (included)
        geo (str): geolocalisation of the search query (Two Uppercase letter (ex: US, CH...) or "" for worldwide)
        gtab_path (str): path to already existing data

    Returns:
    -------
        t (GTAB): GoogleTrendsAnchorBank to use for the queries, consistent with the provided options

    """

    t = gtab.GTAB(dir_path=gtab_path)
    # Create time frame
    timeframe = start_timeframe + " " + end_timeframe
    
    # Set required options
    t.set_options(pytrends_config={"geo": geo, "timeframe": timeframe})  
    
    # Create anchorbank if it doesn't already exist
    t.create_anchorbank() # takes a while to run since it queries Google Trends. 
    
    # We apply the anchorbank
    t.set_active_gtab(f"google_anchorbank_geo={geo}_timeframe={timeframe}.tsv")
    
    return t

def get_json_structure(data):
    out = '{'
    for key, value in data.items():
        if key == 'itemListElement':
            out += '\n\t"' + key + '": [{'
            for key2, value2 in value[0].items():
                if key2 == 'result':
                    out += '\n\t\t"' + key2 + '": {'
                    for key3, value3 in value2.items():
                        out += '\n\t\t\t' + key3 + '": ' + type(value3).__name__
                    out += '\n\t\t}'
                else:
                    out += '\n\t\t"' + key2 + '": ' + type(value2).__name__
            out += '\n\t}, ... ]'
        else:
            out += '\n\t"' + key + '": ' + type(value).__name__

    out += '\n}'
    return out

def load_pickle(datapath):
    
    if sys.version_info[1] >= 8:
        return pd.read_pickle(datapath)
    else:
        import pickle5 as pickle
        with open(datapath, 'rb') as f:
            return pickle.load(f)

        
        
# TO REMOVE
import plotly.tools as pt
import pandas as pd
import chart_studio.tools as tls
import chart_studio.plotly as py
import plotly.graph_objects as go

username = "Arturjssln"
api_key = "H4XMtrMMVkVIcRDyhuc2"
tls.set_credentials_file(username=username, api_key=api_key)

fig = go.Figure()
fig.add_trace(go.Bar(x=[0, 1], y=[mean_pre_june, mean_post_june], name="Average interest", width=0.4))
fig.update_traces(marker_color='#1f78b4')

fig.update_layout(template='plotly_white')
fig.update_layout(title='Figure 2: Terrorism-related articles average interest', xaxis=dict(tickmode='array', tickvales=[0,1],ticktext=['Pre June, 2013', 'Post June, 2013']))
fig.update_yaxes(title_text='Average interest', range=[0,200])
fig.update_layout(legend = dict(x=0.0,y=0.0))



# Get html code for figure
url = py.plot(fig, filename = 'test_bar', auto_open=True)
print(tls.get_embed(url))

EVENT_DATE = pd.to_datetime('2013-06-15')

fig = go.Figure()
terrorism_marged_ts = pd.concat([terrorism_pre_june_ts, terrorism_post_june_ts], axis=0)
fig.add_trace(go.Scatter(x=terrorism_marged_ts.date, y=terrorism_marged_ts.max_ratio, name = 'Total interest (Terrorism)', mode='markers', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_pre_june_ts.date, y=intercept_pre_june + slope_pre_june*x1, name = 'Terrorism-related Trend Pre-June 2013', mode='lines', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_post_june_ts.date, y=intercept_post_june + slope_post_june*x2, name = 'Terrorism-related Trend Post-June 2013', mode='lines', line = dict(color = '#a6cee3', width = 4)))

fig.update_layout(template='plotly_white')
fig.update_layout(title='Figure 3: terrorism- and security-related articles interest trends')
fig.update_xaxes(title_text='Time', tickangle=-45)
fig.update_yaxes(title_text='Total interest by month', range=[0, 150])
fig.add_vline(x=EVENT_DATE, line = dict(color = 'black', width = 4))
fig.add_annotation(x=EVENT_DATE, y=130,
            text="Mid-June 2013",
            showarrow=True,
            arrowhead=4,
            arrowwidth=2,
            ax=100)
fig.update_layout(legend = dict(x = 0.0, y = 0.0))
url = py.plot(fig, filename = 'test_3', auto_open=True)
print(url)
print(tls.get_embed(url))


fig = go.Figure()
terrorism_marged_ts = pd.concat([terrorism_pre_june_ts, terrorism_post_june_ts], axis=0)
fig.add_trace(go.Scatter(x=terrorism_marged_ts.date, y=terrorism_marged_ts.max_ratio, name = 'Total interest (Terrorism)', mode='markers', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_pre_june_ts.date, y=intercept_pre_june + slope_pre_june*x1, name = 'Terrorism-related Trend Pre-June 2013', mode='lines', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_post_june_ts.date, y=intercept_post_june + slope_post_june*x2, name = 'Terrorism-related Trend Post-June 2013', mode='lines', line = dict(color = '#a6cee3', width = 4)))

slope_pre_june_dom, intercept_pre_june_dom, _, _, _ = stats.linregress(domestic_pre_june_ts.index, 
                                                               domestic_pre_june_ts.max_ratio)
slope_post_june_dom, intercept_post_june_dom, _, _, _ = stats.linregress(domestic_post_june_ts.index,
                                                                 domestic_post_june_ts.max_ratio)

domestic_marged_ts = pd.concat([domestic_pre_june_ts, domestic_post_june_ts], axis=0)
fig.add_trace(go.Scatter(x=domestic_marged_ts.date, y=domestic_marged_ts.max_ratio, name = 'Total interest (Security)', mode='markers', line = dict(color = '#33a02c', width = 4)))
fig.add_trace(go.Scatter(x=domestic_pre_june_ts.date, y=intercept_pre_june_dom + slope_pre_june_dom*x1, name = 'Security-related Trend Pre-June 2013', mode='lines', line = dict(color = '#33a02c', width = 4)))

fig.add_trace(go.Scatter(x=domestic_post_june_ts.date, y=intercept_post_june_dom + slope_post_june_dom*x2, name = 'Security-related Trend Post-June 2013', mode='lines', line = dict(color = '#78c879', width = 4)))

fig.update_layout(template='plotly_white')
fig.update_layout(title='Figure 4: terrorism- and security-related articles interest trends')
fig.update_xaxes(title_text='Time', tickangle=-45)
fig.update_yaxes(title_text='Total interest by month', range=[0, 150])
fig.add_vline(x=EVENT_DATE, line = dict(color = 'black', width = 4))
fig.add_annotation(x=EVENT_DATE, y=130,
            text="Mid-June 2013",
            showarrow=True,
            arrowhead=4,
            arrowwidth=2,
            ax=100)
fig.update_layout(legend = dict(x = 0.0, y = 0.0))

url = py.plot(fig, filename = 'test_4', auto_open=True)
print(url)
print(tls.get_embed(url))


# TODO: put clean data here
terrorism_pre_june_ts = terrorism_pre_june_ts
terrorism_post_june_ts = terrorism_post_june_ts
domestic_pre_june_ts = domestic_pre_june_ts
domestic_post_june_ts = domestic_post_june_ts

slope_pre_june, intercept_pre_june, _, _, _ = stats.linregress(terrorism_pre_june_ts.index, 
                                                               terrorism_pre_june_ts.max_ratio)
slope_post_june, intercept_post_june, _, _, _ = stats.linregress(terrorism_post_june_ts.index,
                                                                 terrorism_post_june_ts.max_ratio)


fig = go.Figure()
terrorism_marged_ts = pd.concat([terrorism_pre_june_ts, terrorism_post_june_ts], axis=0)
fig.add_trace(go.Scatter(x=terrorism_marged_ts.date, y=terrorism_marged_ts.max_ratio, name = 'Total interest (Terrorism)', mode='markers', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_pre_june_ts.date, y=intercept_pre_june + slope_pre_june*x1, name = 'Terrorism-related Trend Pre-June 2013', mode='lines', line = dict(color = '#1f78b4', width = 4)))
fig.add_trace(go.Scatter(x=terrorism_post_june_ts.date, y=intercept_post_june + slope_post_june*x2, name = 'Terrorism-related Trend Post-June 2013', mode='lines', line = dict(color = '#a6cee3', width = 4)))

slope_pre_june_dom, intercept_pre_june_dom, _, _, _ = stats.linregress(domestic_pre_june_ts.index, 
                                                               domestic_pre_june_ts.max_ratio)
slope_post_june_dom, intercept_post_june_dom, _, _, _ = stats.linregress(domestic_post_june_ts.index,
                                                                 domestic_post_june_ts.max_ratio)

domestic_marged_ts = pd.concat([domestic_pre_june_ts, domestic_post_june_ts], axis=0)
fig.add_trace(go.Scatter(x=domestic_marged_ts.date, y=domestic_marged_ts.max_ratio, name = 'Total interest (Security)', mode='markers', line = dict(color = '#33a02c', width = 4)))
fig.add_trace(go.Scatter(x=domestic_pre_june_ts.date, y=intercept_pre_june_dom + slope_pre_june_dom*x1, name = 'Security-related Trend Pre-June 2013', mode='lines', line = dict(color = '#33a02c', width = 4)))
fig.add_trace(go.Scatter(x=domestic_post_june_ts.date, y=intercept_post_june_dom + slope_post_june_dom*x2, name = 'Security-related Trend Post-June 2013', mode='lines', line = dict(color = '#78c879', width = 4)))

fig.update_layout(template='plotly_white')
fig.update_layout(title='Figure 5: terrorism- and security-related articles interest trends')
fig.update_xaxes(title_text='Time', tickangle=-45)
fig.update_yaxes(title_text='Total interest by month', range=[0, 150])
fig.add_vline(x=EVENT_DATE, line = dict(color = 'black', width = 4))
fig.add_annotation(x=EVENT_DATE, y=130,
            text="Mid-June 2013",
            showarrow=True,
            arrowhead=4,
            arrowwidth=2,
            ax=100)
fig.update_layout(legend = dict(x = 0.0, y = 0.0))
            
url = py.plot(fig, filename = 'test_5', auto_open=True)
print(url)
print(tls.get_embed(url))

