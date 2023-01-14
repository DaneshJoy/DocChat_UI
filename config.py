import os

import streamlit as st


class Paths:
    TMP_DIR = os.path.join(os.getcwd(), 'temp', st.session_state["username"])
    DOC_DIR = os.path.join(os.getcwd(), 'docs', st.session_state["username"])
    TXT_DIR = os.path.join(os.getcwd(), 'txts', st.session_state["username"])
    CHK_DIR = os.path.join(os.getcwd(), 'chks', st.session_state["username"])
    URL_DIR = os.path.join(os.getcwd(), 'urls', st.session_state["username"])