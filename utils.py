import time
import streamlit as st


def timed_alert(message, wait=3, type_='success', sidebar=False):
    '''
    :params:
        message: string
        wait: integer - default to 2
        type_: string - default to warning (success, warning, erro)
        sidebar: bool - default to False
    '''
    if sidebar:
        placeholder = st.sidebar.empty()
    else:
        placeholder = st.empty()
    if type_ == 'success':
        placeholder.success(message)
    elif type_ == 'warning':
        placeholder.warning(message)
    elif type_ == 'error':
        placeholder.error(message)
    time.sleep(wait)
    placeholder.empty()