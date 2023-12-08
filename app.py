import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


###Page Config###
st.set_page_config(page_title='Job Post Visualisation',
                   layout = 'wide')

###Load CSV Function###
@st.cache_data
def load_csv(path):
    data = pd.read_csv(path)
    return data

###Loading CSVs###
df_clean = load_csv('Cleaned.csv')
df_skill = load_csv('Skills.csv')

###Plotly Graph Functions###
def plot_pie(top, title, ascending=False):
    x = df_skill.sum().sort_values(ascending).head(top)

    fig = go.Figure(data=[go.Pie(
        values=x[1],
        labels =x[0],
        title=title,
        pull= [x.max()],
        textinfo= 'label+value',
        textposition= 'inside',
        color_discrete_sequence = px.colors.sequential.Rainbow
    )])
    fig.update_layout(
        textfont_size = 12, insidetextorentation = 'radial'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_map():
    fig = px.choropleth_mapbox(df,
                               geojson=location,
                               color= pay,
                               color_continuous_scale= 'Rainbow',
                               zoom =3,
                               center={"lat": 37.0902, "lon": -95.7129},
                               opacity=0.5)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)

def plot_gauge(prefix = None,freq= False,highest = False, height= 150):
    if freq:
        results = df_clean.groupby('company_name')['company_name'].value_counts()
        comp = results.idxmax()
        val = results.max()
        title = 'Most frequent recruiting company'
    elif highest:
        results = df_clean.groupby('company_name')['max_yearly'].mean()
        comp = results.idxmax()
        val = results.max()
        title = 'Highest paying company'
    else:
        results = df_clean.groupby('company_name')['min_yearly'].mean()
        comp = results.idxmin()
        val = results.min()
        title = 'Lowest paying company'

    colour = 'red' if val< results.mean() else 'green'

    fig = go.Figure(go.Indicator(
        domain = {'x': [0,1], 'y':[0,1]},
        value = val,
        delta = {'reference': results.mean()},
        title = {'text': f'The {title} is {comp}',
                 'font': 20},
        number = {prefix: prefix},
        mode = 'gauge+number+delta',
        gauge={'axis':{'range': [0,results.max()]},
               'bar': {'color': colour},
               'threshold': {
                   'line': {'color': 'black', 'width': 4},
                   'thickness' : 0.75,
                   'value': val
               }}))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      height = height)
    st.plotly_chart(fig, use_container_width=True)



