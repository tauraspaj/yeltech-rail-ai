import streamlit as st
from common.sql import Sql, Devices, Models
import pandas as pd
from common import fe_lib as lib

models = Models().get_all()

st.set_page_config(layout="wide")
st.title("Devices")

def show_devices_table():
    devices = Devices().get_all()
    devices_df = pd.DataFrame(devices)
    if len(devices) > 0:
        st.dataframe(devices_df.style.format(formatter=lib.decimal_formatter), use_container_width=True)
    else:
        st.write('No devices found.')

# add a button to add a new device
with st.expander('Add New Device'):
    with st.form(key='add_device_form', clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            device_name = st.text_input('Device Name')
            device_depo_location = st.text_input('Depo Location')
            device_latitude = st.number_input('Latitude', format="%.6f")
            device_longitude = st.number_input('Longitude', format="%.6f")
        with col2:
            model = st.selectbox('Model', models)
            prediction_status = st.selectbox('Prediction Status', ['1', '0'])

        submit_button = st.form_submit_button(label='Add Device')

    if submit_button:
        if (len(device_name) < 1 or len(device_depo_location) < 1
                or device_latitude == 0 or device_longitude == 0):
            st.error("All fields are required to be filled in.")
        else:
            sql = "INSERT INTO devices (device_name, depo_location, latitude, longitude, prediction_status, model_id) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (device_name, device_depo_location, device_latitude, device_longitude, prediction_status, model['_model_id'])
            Sql().insert_query(sql, values)
            st.success('Device added successfully!')
            st.balloons()


show_devices_table()
