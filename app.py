import streamlit as st
import requests
import json
from PIL import Image

logo = Image.open('logo.png')
st.image(logo)
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

request_method = st.selectbox('Choose a Request Method', ('GET', 'POST', 'PUT'))
default_api_endpoint = 'ovoc/v1/topology/devices'
api_endpoint = st.text_input('API Endpoint', placeholder=default_api_endpoint)

basicAuthCredentials = (st.secrets["ovoc_username"], st.secrets["ovoc_password"])

if api_endpoint == '':
    api_endpoint=default_api_endpoint

if st.button('Fetch Data'):

    if request_method == 'GET':
        response = requests.get(f"https://tampa-audiocodes-02.chtrse.com/{api_endpoint}", auth=basicAuthCredentials, verify=False)
        data = response.json()
        st.json(data)
        st.download_button("Download data", data=json.dumps(data), file_name="data.json", mime="text/json")