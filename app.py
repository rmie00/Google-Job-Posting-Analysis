
import streamlit as st
###Page Config###
st.set_page_config(page_title='Job Post Visualisation',
                   layout='wide')
from urllib.request import urlopen
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.header('Google Job Postings')

###Load CSV Function###
@st.cache_data
def load_csv(path):
    data = pd.read_csv(path)
    return data


###Loading CSVs###
df_clean= load_csv('Cleaned.csv')
df_skill = load_csv('Skills.csv')

###Extra Cleaning###
# Mean of expected pay
df_clean['high_low_mean'] = (df_clean['min_yearly'] + df_clean['max_yearly']) / 2

with st.expander('DataFrame'):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Cleaned Data Frame')
        st.dataframe(df_clean)

    with col2:
        st.subheader('Skill Required Data Frame')
        st.dataframe(df_skill)
###Plotly Graph Functions###
def plot_pie(top, title):
    x = df_skill.sum().sort_values(ascending=False).head(top)
    pul = [0.2] + [0] * (len(x.to_list()) - 1)

    fig = go.Figure(data=[go.Pie(
        values=x,
        labels=x.index,
        pull=pul,
        # color_discrete_sequence = px.colors.sequential.Rainbow,
        textinfo='label+value',
        textposition='inside'
    )])
    fig.update_traces(textposition='inside',
                      textinfo='percent+label+value')
    fig.update_layout(title=title,
                      uniformtext_minsize=12,
                      uniformtext_mode='hide',
                      margin={"r": 0, "t": 35, "l": 0, "b": 0},
                      height=400)

    st.plotly_chart(fig,
                    use_container_width=True)


def plot_map():
    temp_df = df_clean.groupby('state')['high_low_mean'].agg(['mean', 'count']).reset_index()
    temp_df.columns = ['State', 'Mean Salary', 'Number Of Job Openings']
    temp_df['Mean Salary'] = temp_df['Mean Salary'].round(2)

    fig = px.choropleth(temp_df,locationmode="USA-states", locations=temp_df['State'],color = "Mean Salary",
                               scope ='usa',
                               color_continuous_scale="Blues",
                              range_color=(temp_df['Mean Salary'].min(), temp_df['Mean Salary'].max()),
                               labels={'freq': 'Mean Salary'}
                               )
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0},
                      title_text='Mean Salary Offerings <br>By State',height = 500,
                      geo=dict(
                          scope='usa',
                          projection=go.layout.geo.Projection(type='albers usa')
                      ))
    st.plotly_chart(fig,
                    use_container_width=True)

def plot_gauge(type=None, prefix=None):
    if type == 'comp':
        results = df_clean.groupby('company_name')['company_name'].value_counts()
        comp = results.idxmax()
        val = results.max()
        title = 'Most frequent recruiting company'
    elif type == 'high':
        results = df_clean.groupby('company_name')['max_yearly'].mean()
        comp = results.idxmax()
        val = results.max()
        title = 'Highest paying company'
    elif type == 'low':
        results = df_clean.groupby('company_name')['min_yearly'].mean()
        comp = results.idxmin()
        val = results.min()
        title = 'Lowest paying company'
    else:
        raise TypeError(f"Only 'comp', 'high', 'low'")

    colour = 'red' if val < results.mean() else 'blue'

    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=val,
        delta={'reference': results.mean(),
               'increasing': {'color': 'blue'},
               'decreasing': {'color': 'red'}},
        number={'prefix': prefix},
        mode='gauge+number+delta',
        gauge={'axis': {'range': [0, results.max()]},
               'bar': {'color': colour},
               'threshold': {
                   'line': {'color': 'black', 'width': 4},
                   'thickness': 0.75,
                   'value': val}},
        ## Setting title to be bold
        title={'text': f'<b>The {title} is {comp}</b>',
               'font': {'size': 15}}
    ))
    fig.update_layout(margin={"r": 40, "t": 30, "l": 40, "b": 0},
                      height=250)

    st.plotly_chart(fig,
                    use_container_width=True,
                    height=170)


def plot_bar(type, xtitle=None, ytitle=None, titl=None, height=400):
    if type == 'pay':
        quartiles = [df_clean['high_low_mean'].quantile(q) for q in [0, 0.25, 0.5, 0.75, 1]]
        var = ['Bottom 25%', 'Range 25%-50%', 'Range 50%-75%', 'Top 25%']
        ivar = [
            df_clean.loc[(df_clean['high_low_mean'] >= quartiles[0]) & (
                        df_clean['high_low_mean'] < quartiles[1]), 'high_low_mean'].mean(),
            df_clean.loc[(df_clean['high_low_mean'] >= quartiles[1]) & (
                        df_clean['high_low_mean'] < quartiles[2]), 'high_low_mean'].mean(),
            df_clean.loc[(df_clean['high_low_mean'] >= quartiles[2]) & (
                        df_clean['high_low_mean'] < quartiles[3]), 'high_low_mean'].mean(),
            df_clean.loc[(df_clean['high_low_mean'] >= quartiles[3]) & (
                        df_clean['high_low_mean'] <= quartiles[4]), 'high_low_mean'].mean()
        ]
    elif type == 'freq':
        results = df_clean['schedule_type'].value_counts()
        var = results.index
        ivar = results

    elif type == 'area':
        results = df_clean.groupby('state')['high_low_mean'].mean().sort_values(ascending=False)
        var = results.index[0:10]
        ivar = results[0:10]
    else:
        raise TypeError(f"Only 'pay', 'freq;, 'area'")

    fig = px.bar(x=var,
                 y=ivar,
                 text_auto='.2f',
                 color=ivar,
                 title=titl)

    fig.update_layout(margin={"r": 0, "t": 35, "l": 0, "b": 0},
                      xaxis_title=f'<b>{xtitle}</b>',
                      yaxis_title=f'<b>{ytitle}</b>',
                      height=height)
    st.plotly_chart(fig,
                    use_container_width=True)


map, top_right_corner = st.columns((1, 1.4))

bottom_left, bottom_right = st.columns((2, 1))

with map:
    plot_map()

with top_right_corner:
    top_corner_left, top_corner_right = st.columns(2)

    top_corner_left_bottom, top_corner_right_bottom = st.columns(2)

    with top_corner_right:
        plot_gauge('comp')
        st.markdown('')

    with top_corner_left:
        plot_gauge('high')
        st.markdown('')

    with top_corner_left_bottom:
        plot_gauge('low')
        st.markdown('')

    with top_corner_right_bottom:
        plot_bar('freq', xtitle='Type of Employment', ytitle='Frequency', height=250, titl='Types of employment')
        st.markdown('')

with bottom_left:
    col_left, col_right = st.columns((1.3, 1))

    with col_left:
        plot_pie(20, '20 Most Demanded Skills In Data Analysis Jobs')

    with col_right:
        plot_bar('area', xtitle='Location', ytitle='Compensation Offered',
                 titl='Salary Offers')

with bottom_right:
    plot_bar('pay', xtitle='Mean Pay of Jobs', ytitle='Average Salary In Range', titl='Salary Mean Distribution')
