import streamlit as st
import requests
import json

st.header("OVOC Audiocodes API")

request_method = st.selectbox('Choose a Request Method', ('GET', 'POST', 'PUT'))
api_endpoint = st.text_input('API Endpoint', placeholder='ovoc/v1/topology/statistics/devices')

basicAuthCredentials = (st.secrets["ovoc_username"], st.secrets["ovoc_password"])

if api_endpoint == '':
    api_endpoint='ovoc/v1/topology/statistics/devices'

if st.button('Fetch Data'):

    if request_method == 'GET':
        response = requests.get(f"https://tampa-audiocodes-02.chtrse.com/{api_endpoint}", auth=basicAuthCredentials, verify=False)
        data = response.json()
        st.json(data)
        st.download_button("Download data", data=json.dumps(data), file_name="data.json", mime="text/json")