import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import numpy as np
from local_components import card_container
from streamlit_shadcn_ui import slider, input, textarea, radio_group, switch
import plotly.express as px
from streamlit_tags import st_tags
from streamlit_discourse import st_discourse


st.set_page_config(
    page_title="Data in our World",
    page_icon="chart_with_upwards_trend",
    layout="wide",

)

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"][aria-expanded="true"]{
      display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# TITLE OF THE WEBPAGE
st.header("Tariffs Before and After the Trump Administration", divider="gray")

# INGEST FILES
data_before_bar = pd.read_csv('./assets/0_data/BeforeTrump_Bar.csv')
data_before = pd.read_csv('./assets/0_data/BeforeTrump.csv')

# FUNCTION FOR FORMATTING % ON COLUMNS    
def format_percentage(df,column_name):  
    df[column_name] = df[column_name].str.rstrip('%').astype('float') / 100.0
    return df

data_before_bar=format_percentage(data_before_bar,'Simple_Average')
data_before=format_percentage(data_before,'Tariffs_US')
data_before=format_percentage(data_before,'Tariffs_Partner')

data_before_bar['Simple_Average']=data_before_bar['Simple_Average']*100

# BEFORE AND AFTER TRUMP ADMINISTRATION
# st.markdown("<h3 style='text-align: center; primaryColor: white; secondaryColor: black;' >" \
# "Tariffs Before & After the Trump Administration</h3>", unsafe_allow_html=True)

country_list =['Brazil', 'India', 'Thailand','Vietnam', 'Indonesia','China', 'Malaysia','EU', 'Japan','South Korea', 'Canada','Israel', 'Colombia','Mexico', 'Singapore']

countries_picked = st_tags(
    label='Enter Trade Partner(s) - only top 15 trading partners available:',
    text='Select Countries',
    value=country_list,
    suggestions=country_list,
    maxtags=15,
    key="countries")


data_before_bar = data_before_bar[data_before_bar['Country'].isin(countries_picked)]

fig = px.bar(data_before_bar, 
             x='Country',
             y='Simple_Average',
             color='Country Charging The Tariff',
             barmode='group',
             text_auto='.2',
             labels={'Simple_Average':'Simple Avg %'},
             range_y=[0,40]
             )
fig.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
fig.update_xaxes(tickangle=270)
fig.update_layout(legend=dict(
    orientation="v",
    yanchor="bottom",
    y=0.75,
    xanchor="right",
    x=1.00
))
# fig.update_layout(legend_traceorder="reversed")
st.plotly_chart(fig)

data_before_table=pd.read_csv('./assets/0_data/BeforeTrump_Table.csv')
data_before_table=data_before_table[data_before_table['Country'].isin(countries_picked)]
st.dataframe(data_before_table, hide_index=True,row_height=20) 

st.caption("""<u>NOTES</u><br>
        1. Simple Applied Average figures were used. The Simple Applied Average was preferred to the MFN Simple Average because it accounts for special trade agreements in place (eg - NAFTA) between countries.
           The Simple Applied Average was preferred to the Weighted Applied Average because the Weighted Applied Average incorporates trade volume which is driven by consumer behavior and cannot be directly controlled by government. 
           The Simple Applied Average appears to be the closest approximation of tariff rates that goverments charge in this context. Detailed definitions available on <a href='https://wits.worldbank.org/Bilateral-Tariff-Technical-Note.html'>this link</a>.<br>
        2. Year 2022 figures were used because this was the most recent applied simple average tariff rate computation found on WITS.
           WTO and more recent data sources that provide 2023 and 2024 figures do not compute a Simple Applied Average Rate for tariffs.<br> 
        3. Current US tariff summary average is based on <a href='https://www.bbc.com/news/articles/c5ypxnnyg7jo'>the BBC</a> figures released April 10, 2025.<br>
        4. US current tariff to China is 140 percent and China's retaliation rate is 125 percent. This is not depicted in the graph as it is too large, instead, it is noted in the below table<br>
        5. Source data for 2022 Simple Applied Avgs were taken from <a href='https://wits.worldbank.org/CountryProfile/en/Country/USA/Year/2022/TradeFlow/EXPIMP'>WITS country profile links</a> specifying trade partners. Downloads were performed for each country's data. This data can be replicated by clicking on 'Show More Columns' and checking 'AHS Simple Average (%)' under 'Tariff - Effectively Applied'""" , unsafe_allow_html=True)


url='https://wits.worldbank.org/'
st.text("Based on data from [WITS](%s). The latest comprehensive data that provides 'Simple Applied Average Rates' prior to the Trump tariffs is 2022. " \
"The purpose of this data is to provide information around how much each government charged in tariffs to the United States before and after April 11, 2025. We chose this date because the Trump administration" \
" imposed their tariffs on April 10th and the following day (April 11th) includes retaliation tariff rates of US trade partners." % url)

# US COMPARISON AFTER TRUMP
st.markdown("<h3 style='text-align: center; primaryColor: white; secondaryColor: black;' >Tariffs Charged by US as of April 10, 2025 vs 2022</h3>", unsafe_allow_html=True)

data_after = pd.read_csv('./assets/0_data/AfterTrump.csv')
data_after = format_percentage(data_after,'Simple_Average')
data_after['Simple_Average']=data_after['Simple_Average']*100

fig2 = px.bar(data_after, 
             x='Country',
             y='Simple_Average',
             color='US Tariff Charged',
             barmode='group',
             text_auto='.2',
             labels={'Simple_Average':'Simple Avg %'},
             range_y=[0,40]
             )
fig2.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
fig2.update_xaxes(tickangle=270)
fig2.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=0.84,
    xanchor="right",
    x=1.00
))

st.plotly_chart(fig2)

st.caption("Updated as of April 10, 2025")



