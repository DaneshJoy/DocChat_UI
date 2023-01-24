import time
import yaml

import streamlit as st
import streamlit_authenticator as stauth


# --- USER AUTHENTICATION ---
def auth():
    with open('utils/creds.yaml') as file:
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


def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value
        print(f'added session state "{key}" with value "{value}"')
