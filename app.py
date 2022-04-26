import streamlit as st
import requests
import json
from PIL import Image

logo = Image.open('logo.png')

def get_data(target, endpoint):
    response = requests.get(f"{target}{endpoint}", auth=basicAuthCredentials, verify=False)
    return response.json()

st.set_page_config(page_title='OVOC Audiocodes API', page_icon=logo)
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
basicAuthCredentials = (st.secrets["ovoc_username"], st.secrets["ovoc_password"])

data = get_data(ems_system, default_api_endpoint)
device = st.text_input("Search a Device", placeholder="69.58.145.105")
devices = data["devices"]

if st.button('Search'):

    st.subheader(f"Available Devices ({devices.length} search results)")

    for i, d in enumerate(devices):
        if i < 5:
            with st.expander(f"{d['description']}"):
                device_endpoint = d["url"]
                detailed_data = get_data(ems_system, device_endpoint)
                st.json(detailed_data)
                st.download_button("Download data", data=json.dumps(detailed_data), file_name="data.json", mime="text/json")
