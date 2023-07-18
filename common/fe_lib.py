from decimal import Decimal
import streamlit as st

def decimal_formatter(x):
    if isinstance(x, Decimal):
        return x
    return x

def add_device():
    with st.form(key='add_device_form'):
        col1, col2 = st.columns(2)
        with col1:
            device_name = st.text_input('Device Name')
            device_name = st.text_input('Depo Location')
            device_latitude = st.number_input('Latitude', format="%.6f")
            device_longitude = st.number_input('Longitude', format="%.6f")
        with col2:
            prediction_status = st.selectbox('Prediction Status', ['1', '0'])

        # Buttons
        submit_button = st.form_submit_button(label='Add Device')
        # cancel_button = st.form_submit_button('Cancel')

    if submit_button:
        st.success('Device added successfully.')


