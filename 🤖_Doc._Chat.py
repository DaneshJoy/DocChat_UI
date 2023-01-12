import os
import yaml
import time
from functools import partial
import streamlit as st
from utils import timed_alert
import streamlit_authenticator as stauth
import requests


st.set_page_config(layout="wide")

def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def auth():
    with open('creds.yaml') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            st.error(exc)
            return

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )

        # location : 'sidebar' or 'main'
        name, authentication_status, username = authenticator.login('Login', 'main')

        if st.session_state['authentication_status']:
            
            return authenticator

        elif st.session_state['authentication_status'] == False:
            timed_alert('Invalid username or password', type_='error')
        # elif st.session_state['authentication_status'] == None:
        #     timed_alert('Please enter your username and password')
        
        return False
    
def send_question_to_api(question):
    timed_alert(f"Generating answer ...\n Please wait")

def send_link_to_api(link):
    timed_alert(f"Processing URL ...\n Please wait")



# set_state_if_absent("authorized", False)
authenticator = auth()
if authenticator:
    # TODO: upload_doc: only uploads and returns list of uploaded_files
    # TODO: submit_docs: check if new/exists and save + proper messages + clear uploaded list
    
    st.title('Doc. Chat')
    st.markdown("##### Intelligent Question-Answering on Documents")
    # st.markdown('---')
    st.text_input(label="Query", value="", placeholder="Enter your question",
        key="placeholder", label_visibility='hidden')
    st.button('Answer', on_click=partial(send_question_to_api, None))
    
    for _ in range(2):
        st.sidebar.write("")
        
    with st.sidebar.expander("About the App"):
        st.write("""
        Intelligent Question-Answering and Chat on Documents
        """)
    
    st.markdown('---')

    # st.markdown(
    #     f"""
    #     <style>
    #         [data-testid="stSidebarNav"] + div {{
    #             position:relative;
    #             bottom: 0;
    #             height:50%;
    #         }}
    #     </style>
    #     """,
    #     unsafe_allow_html=True,
    # )
    
    for _ in range(15):
        st.sidebar.write("")

    st.sidebar.markdown('---')
    st.sidebar.write(f'Logged in as "*{st.session_state["name"]}*"')
    authenticator.logout('Logout', 'sidebar')
    # files_list = st.selectbox('Select a content', options=file_names)
