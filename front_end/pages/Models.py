import streamlit as st
from common.sql import Sql, Devices, Models
import pandas as pd
from common import fe_lib as lib

st.set_page_config(layout="wide")
st.title("Models")


def show_models_table():
    models = Models().get_all()

    if len(models) > 0:
        st.dataframe(models, use_container_width=True)
    else:
        st.write('No devices found.')

show_models_table()
