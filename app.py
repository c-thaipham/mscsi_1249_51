from ipaddress import ip_address
import streamlit as st
import requests
import json
from PIL import Image

def get_data(target, endpoint):
    response = requests.get(f"{target}{endpoint}", auth=basicAuthCredentials, verify=False)
    return response.json()

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

devices = get_data(ems_system, default_api_endpoint)["devices"]
calls = get_data(ems_system, calls_api_endpoint)["calls"]
device = st.text_input("Search a Device", placeholder="69.58.145.105")

if st.button('Search'):

    st.subheader(f"Available Devices ({len(devices)} search results)")

    for i, d in enumerate(devices):
        if i < 5:
            with st.expander(f"{d['description']}"):
                with st.expander("Device Info"):
                    st.write("Device Info")
                with st.expander("IP Address"):
                    ip_address = d["ipAddress"]
                    st.json(ip_address)
                with st.expander("Calls Info"):
                    st.write("Calls Info")
                

                # device_endpoint = d["url"]
                # detailed_data = get_data(ems_system, device_endpoint)
                # st.json(detailed_data)
                # st.download_button("Download data", data=json.dumps(detailed_data), file_name="data.json", mime="text/json")
