import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import numpy as np
from local_components import card_container
from streamlit_shadcn_ui import slider, input, textarea, radio_group, switch
import plotly.express as px
from streamlit_tags import st_tags

st.set_page_config(
    page_title="Data in our World",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

# TITLE OF THE WEBPAGE
st.header("Tariffs Before and After the Trump Administration", divider="gray")

def read_csv_with_percentage(file_path, column_name):
    df = pd.read_csv(file_path)
    df[column_name] = df[column_name].str.rstrip('%').astype('float') / 100.0
    return df

data_before_bar=read_csv_with_percentage('BeforeTrump_Bar.csv','Simple_Average')
data_before=read_csv_with_percentage('BeforeTrump.csv','Tariffs_US')
data_before['Tariffs_Partner']=data_before['Tariffs_Partner'].str.rstrip('%').astype('float') / 100.0

data_before_bar['Simple_Average']=data_before_bar['Simple_Average']*100

url='https://wits.worldbank.org/'
st.caption("Based on data from [WITS](%s). The latest comprehensive data that provides 'Simple Applied Average Rates' prior to the Trump tariffs is 2022. " \
"The purpose of this data is to provide information around how much each government charged in tariffs to the United States before and after April 11, 2025. We chose this date because the Trump administration" \
"imposed their tariffs on April 10th and the following day (April 11th) includes retaliation tariff rates of US trade partners." % url)

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

st.caption("""
        1. Simple Applied Average figures were used. The Simple Applied Average was preferred to the MFN Simple Average because it accounts for special trade agreements in place (eg - NAFTA) between countries.
           The Simple Applied Average was preferred to the Weighted Applied Average because the Weighted Applied Average incorporates trade volume which is driven by consumer behavior and cannot be directly controlled by government. 
           The Simple Applied Average appears to be the closest approximation of tariff rates that goverments charge in this context. Detailed definitions available on <a href='https://wits.worldbank.org/Bilateral-Tariff-Technical-Note.html'>this link</a>.
        2. Year 2022 figures were used because this was the most recent applied simple average tariff rate computation found on WITS.
           WTO and more recent data sources that provide 2023 and 2024 figures do not compute a Simple Applied Average Rate for tariffs.<br> 
        3. Current US tariff summary average is based on <a href='https://www.bbc.com/news/articles/c5ypxnnyg7jo'>the BBC</a> figures released April 10, 2025.<br>
        4. US current tariff to China is 140 percent and China's retaliation rate is 125 percent. This is not depicted in the graph as it is too large, instead, it is noted in the below table""" , unsafe_allow_html=True)


data_before_table=pd.read_csv('BeforeTrump_Table.csv')
data_before_table=data_before_table[data_before_table['Country'].isin(countries_picked)]
st.dataframe(data_before_table, hide_index=True,row_height=20) 


# US COMPARISON AFTER TRUMP
st.markdown("<h3 style='text-align: center; primaryColor: white; secondaryColor: black;' >Tariffs Charged by US as of April 10, 2025</h3>", unsafe_allow_html=True)

data_after = read_csv_with_percentage('AfterTrump.csv','Simple_Average')
data_after['Simple_Average']=data_after['Simple_Average']*100

fig2 = px.bar(data_after, 
             x='Country',
             y='Simple_Average',
             color='US Tariff Charged',
             barmode='group',
             text_auto='.2',
             labels={'Simple_Average':'Simple Avg %'},
             range_y=[0,14]
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





# ui.badges(badge_list=[("shadcn", "default"), ("in", "secondary"), ("streamlit", "destructive")], class_name="flex gap-2", key="main_badges1")

# st.dataframe(
#     data_before,
#     column_config={
#         "Country": "Trade Partner",
#         "Tariffs_US": st.column_config.NumberColumn("Tariff Charged By the US"),
#         "Tariffs_Partner": st.column_config.NumberColumn("Tariff Charged By Partner")
#     },
#     height=500,
#     hide_index=True,
# )

# with ui.element("div", className="flex gap-2", key="buttons_group1"):
#     ui.element("button", text="Get Started", className="btn btn-primary", key="btn1")
#     ui.element("link_button", text="Github", url="https://github.com/ObservedObserver/streamlit-shadcn-ui", variant="outline", key="btn2")

# st.subheader("Dashboard")

# ui.tabs(options=['Overview', 'Analytics', 'Reports', 'Notifications'], default_value='Overview', key="main_tabs")

# ui.date_picker(key="date_picker1")

# cols = st.columns(3)
# with cols[0]:
#     # with ui.card():
#     #     ui.element()
#     ui.card(title="Total Revenue", content="$45,231.89", description="+20.1% from last month", key="card1").render()
# with cols[1]:
#     ui.card(title="Subscriptions", content="+2350", description="+180.1% from last month", key="card2").render()
# with cols[2]:
#     ui.card(title="Sales", content="+12,234", description="+19% from last month", key="card3").render()

# def generate_sales_data():
#     np.random.seed(0)  # For reproducible results
#     months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#     sales = np.random.randint(1000, 5000, size=len(months))
#     return pd.DataFrame({'Month': months, 'Sales': sales})

# with card_container(key="chart1"):
#     st.vega_lite_chart(generate_sales_data(), {
#         'mark': {'type': 'bar', 'tooltip': True, 'fill': 'rgb(173, 250, 29)', 'cornerRadiusEnd': 4 },
#         'encoding': {
#             'x': {'field': 'Month', 'type': 'ordinal'},
#             'y': {'field': 'Sales', 'type': 'quantitative', 'axis': {'grid': False}},
#         },
#     }, use_container_width=True)

# # Sample data
# data = [
#     {"invoice": "INV001", "paymentStatus": "Paid", "totalAmount": 500, "paymentMethod": "Credit Card"},
#     {"invoice": "INV002", "paymentStatus": "Unpaid", "totalAmount": 200, "paymentMethod": "Cash"},
#     {"invoice": "INV003", "paymentStatus": "Paid", "totalAmount": 150, "paymentMethod": "Debit Card"},
#     {"invoice": "INV004", "paymentStatus": "Unpaid", "totalAmount": 350, "paymentMethod": "Credit Card"},
#     {"invoice": "INV005", "paymentStatus": "Paid", "totalAmount": 400, "paymentMethod": "PayPal"},
#     # Add more records as needed
# ]

# # Creating a DataFrame
# invoice_df = pd.DataFrame(data)

# with card_container(key="table1"):
#     ui.table(data=invoice_df, maxHeight=300)


# ui_result = ui.button("Button", key="btn")
# st.write("UI Button Clicked:", ui_result)


# # Slider Component
# slider_value = slider(default_value=[20], min_value=0, max_value=100, step=2, label="Select a Range", key="slider1")
# st.write("Slider Value:", slider_value)

# # Input Component
# input_value = input(default_value="Hello, Streamlit!", type='text', placeholder="Enter text here", key="input1")
# st.write("Input Value:", input_value)

# # Textarea Component
# textarea_value = textarea(default_value="Type your message here...", placeholder="Enter longer text", key="textarea1")
# st.write("Textarea Value:", textarea_value)

# # Radio Group Component
# radio_options = [
#     {"label": "Option A", "value": "A", "id": "r1"},
#     {"label": "Option B", "value": "B", "id": "r2"},
#     {"label": "Option C", "value": "C", "id": "r3"}
# ]
# radio_value = radio_group(options=radio_options, default_value="B", key="radio1")
# st.write("Selected Radio Option:", radio_value)

# # Switch Component
# switch_value = switch(default_checked=True, label="Toggle Switch", key="switch1")
# st.write("Switch is On:", switch_value)

# st.subheader("Alert Dialog")
# trigger_btn = ui.button(text="Trigger Button", key="trigger_btn")
# ui.alert_dialog(show=trigger_btn, title="Alert Dialog", description="This is an alert dialog", confirm_label="OK", cancel_label="Cancel", key="alert_dialog1")