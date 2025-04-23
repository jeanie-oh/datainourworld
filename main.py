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

st.header("Apps for Data in our World", divider="gray")
