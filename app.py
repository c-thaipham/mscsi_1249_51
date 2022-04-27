from ipaddress import ip_address
from multiprocessing.sharedctypes import Value
import streamlit as st
import requests
import json
from PIL import Image
import pandas as pd
import numpy as np

def get_data(target, endpoint):
    response = requests.get(f"{target}{endpoint}", auth=basicAuthCredentials, verify=False)
    return response.json()

def validate_ip_address(address):
    try:
        return ip_address(address)
    except ValueError:
        return False

def display_custom_text(message):
    custom_text = f'<p style="font-family:sans-serif; color:Red; font-size: 20px;">{message}</p>'
    st.markdown(custom_text, unsafe_allow_html=True)

def create_series(series_data:list):
    data = np.array(series_data)
    s = pd.Series(data)
    return s

def create_dataframe(**column_data):
    data = {**column_data}
    df = pd.DataFrame(data)
    return df

        
        
    

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

logo = Image.open('logo.png')

# st.set_page_config(page_title='OVOC Audiocodes API', page_icon=logo)
st.header("OVOC Audiocodes API")

ems_system = st.selectbox('Choose an EMS System',
(
    'https://tampa-audiocodes-02.chtrse.com',
    'https://tampa-audiocodes-04.chtrse.com',
    'https://tampa-audiocodes-03.chtrse.com',
    'https://austx-audiocodeshicap.chtrse.com',
    'https://austx-audiocodeshv.chtrse.com',
    'https://austx-audiocodestrunk.chtrse.com',
    'https://austx-ac-overflow.chtrse.com',
    'https://austx-ac-cluster.dmz.chtrse.com')
)

request_method = 'GET'
default_api_endpoint = '/ovoc/v1/topology/devices'
calls_api_endpoint = '/ovoc/v1/callsMonitor/calls/'
basicAuthCredentials = (st.secrets["ovoc_username"], st.secrets["ovoc_password"])

device_placeholder = "e.g. 11.11.111.111 or  +16012345678"
devices_series = create_series([d["url"] for d in get_data(ems_system, default_api_endpoint)["devices"]])
device = st.text_input("Find a Device", placeholder=device_placeholder)
search_by = st.radio(
     "Search by",
     ('IP Address', 'Source Number', 'Destination Number'))
    
default_ip_address = "71.78.243.74"
    

if search_by in ['Source Number', 'Destination Number']:
    pass

if st.button('Search'):
    if search_by == 'IP Address':
        if not validate_ip_address(device):
            display_custom_text("Please enter a valid IP Address")
        else:
            st.write(devices_series)