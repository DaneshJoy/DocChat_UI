import os

import streamlit as st


class Paths:
    TMP_DIR = os.path.join(os.getcwd(), 'users', st.session_state["username"], 'temp')
    DOC_DIR = os.path.join(os.getcwd(), 'users', st.session_state["username"], 'docs')
    TXT_DIR = os.path.join(os.getcwd(), 'users', st.session_state["username"], 'txts')
    CHK_DIR = os.path.join(os.getcwd(), 'users', st.session_state["username"], 'chks')
    URL_DIR = os.path.join(os.getcwd(), 'users', st.session_state["username"], 'urls')