import yaml
from functools import partial

import streamlit as st
import streamlit_authenticator as stauth

from utils.utils import auth
from utils.utils import timed_alert
from utils.html_codes import *
from utils.api import send_question_to_api
from utils.utils import set_state_if_absent


st.set_page_config(page_title="Doc. Chat", page_icon="🤖", layout="wide",
                   menu_items={'About': "### Doc. Chat app!"})

st.markdown(HIDE_ST, unsafe_allow_html=True)


def logout(authenticator):
    for _ in range(15):
        st.sidebar.write("")
    st.sidebar.markdown('---')
    st.sidebar.write(f'Logged in as "*{st.session_state["name"]}*"')
    authenticator.logout('Logout', 'sidebar')


def main():
    authenticator = auth()
    if authenticator:
        st.markdown(SHOW_BAR, unsafe_allow_html=True)
        # set_state_if_absent('question', None)

        st.title('Doc. Chat')
        st.markdown("##### Intelligent Question-Answering on Documents")
        # st.markdown('---')
        st.text_input(label="Query", value="", placeholder="Enter your question",
                      key="question", label_visibility='hidden', on_change=send_question_to_api)
        st.button('Answer', on_click=send_question_to_api)

        logout(authenticator)
    else:
        st.markdown(HIDE_BAR, unsafe_allow_html=True)


main()
