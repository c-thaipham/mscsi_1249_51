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

device_placeholder = "e.g. 11.11.111.111 or  +16012345678"
devices = get_data(ems_system, default_api_endpoint)["devices"]
calls = get_data(ems_system, calls_api_endpoint)
device = st.text_input("Search a Device", placeholder=device_placeholder)
search_by = st.radio(
     "Search by",
     ('IP Address', 'Source Number', 'Destination Number'))
    
if search_by == 'IP Address':
    pass
if search_by in ['Source Number', 'Destination Number']:
    pass

if st.button('Search'):

    st.subheader(f"Search Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Devices", f"{len(devices)}")
    col2.metric("Source Numbers", f"{0}")
    col3.metric("Destination Numbers", "10")

    for i, d in enumerate(devices):
        if i < 5:
            with st.expander(f"{d['description']}"):
                with st.container():
                    # Find IP Address of the device and display it
                    device_endpoint = d["url"]
                    device_data = get_data(ems_system, device_endpoint)
                    ip_address = device_data["ipAddress"]
                    st.subheader(f"IP Address: {ip_address}")


                # st.download_button("Download data", data=json.dumps(detailed_data), file_name="data.json", mime="text/json")
    st.json(calls)