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
def plot_pie(data, top, title, su=False, ascending=False):
    if su:
        x = data.sum().sort_values(ascending).head(top)
    else:
        x = data.sort_values(ascending).head(top)
    fig = go.Figure(data=[go.Pie(
        values=x[1],
        labels =x[0],
        title=title,
        pull= [val.max()],
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


