from ipaddress import ip_address
from multiprocessing.sharedctypes import Value
import streamlit as st
import requests
import json
from PIL import Image

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
calls = get_data(ems_system, calls_api_endpoint)["calls"]
device = st.text_input("Find a Device", placeholder=device_placeholder)
search_by = st.radio(
     "Search by",
     ('IP Address', 'Source Number', 'Destination Number'))
    
default_ip_address = "71.78.243.74"
    

if search_by in ['Source Number', 'Destination Number']:
    pass

if st.button('Search'):
    
    
    # st.subheader(f"Search Results")
    # col1, col2, col3 = st.columns(3)
    # col1.metric("Devices", f"{len(devices)}")
    # col2.metric("Source Numbers", f"{0}")
    # col3.metric("Destination Numbers", "10")
    if search_by == 'IP Address':
        if device is None or device == '':
            device = default_ip_address

        if not validate_ip_address(device):
            display_custom_text("Please enter a valid IP Address")
        else:
            # Find IP Address of the device and display it
            for d in devices:
                device_api_endpoint = d["url"]
                device_data = get_data(ems_system, device_api_endpoint)
                device_ip_address = device_data["ipAddress"]
                            
                if device_ip_address == device:
                    with st.expander(f"{d['description']}"):
                        with st.container():
                            device_id = d['id']
                            st.subheader(f"Device ID: {device_id}")
                            st.subheader(f"IP Address: {device_ip_address}")

                            for c in calls:
                                call_api_endpoint = c["url"]
                                call_data = get_data(ems_system, call_api_endpoint)
                                call_reporting_node_id = call_data["reportingNodeId"]

                                if call_reporting_node_id == device_id:
                                    st.json(call_data)
                            
                            
                    break


                # st.download_button("Download data", data=json.dumps(detailed_data), file_name="data.json", mime="text/json")
    # for i, c in enumerate(calls):
    #     if i < 5:
    #         call_api_endpoint = c["url"]
    #         call_data = get_data(ems_system, call_api_endpoint)
    #         st.json(call_data)