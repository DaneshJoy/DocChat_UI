import time
import streamlit as st


def timed_alert(message, wait=2, type_='success'):
    '''
    :params:
        message: string
        wait: integer - default to 2
        type_: string - default to warning (success, warning, erroe)
    '''
    placeholder = st.sidebar.empty()
    if type_ == 'success':
        placeholder.success(message)
    elif type_ == 'warning':
        placeholder.warning(message)
    elif type_ == 'error':
        placeholder.error(message)
    time.sleep(wait)
    placeholder.empty()