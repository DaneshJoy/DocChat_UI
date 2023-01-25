import os

import streamlit as st


class Paths:
    TMP_DIR = os.path.join(os.getcwd(), 'users', st.session_state["username"], 'temp')
    DOC_DIR = os.path.join(os.getcwd(), 'users', st.session_state["username"], 'docs')
    TXT_DIR = os.path.join(os.getcwd(), 'users', st.session_state["username"], 'txts')
    CHK_DIR = os.path.join(os.getcwd(), 'users', st.session_state["username"], 'chks')
    URL_DIR = os.path.join(os.getcwd(), 'users', st.session_state["username"], 'urls')

class Urls:
    # CHK_URL = 'http://54.242.28.52/doc/send_chunks'
    # CLR_URL = 'http://54.242.28.52/doc/clear'
    # RTD_URL = 'http://54.242.28.52/doc/get_related_contents'

    CHK_URL = 'http://localhost:8088/doc/send_chunks'
    CLR_URL = 'http://localhost:8088/doc/clear'
    RTD_URL = 'http://localhost:8088/doc/get_related_contents'