import os
import shutil
import requests

import streamlit as st

from utils.config import Paths, Urls
from utils.utils import timed_alert


def clear_docs():
    btn_container.empty()
    with btn_container:
        st.write('⌛ Please wait...')
        with st.spinner('Clearing all documents...'):
            # if os.path.exists(Paths.TMP_DIR):
            #     shutil.rmtree(Paths.TMP_DIR)
            if os.path.exists(Paths.DOC_DIR):
                shutil.rmtree(Paths.DOC_DIR)
            if os.path.exists(Paths.TXT_DIR):
                shutil.rmtree(Paths.TXT_DIR)
            if os.path.exists(Paths.CHK_DIR):
                shutil.rmtree(Paths.CHK_DIR)
            if os.path.exists(Paths.URL_DIR):
                shutil.rmtree(Paths.URL_DIR)

            if not os.path.exists(Paths.TMP_DIR):
                os.makedirs(Paths.TMP_DIR)
            if not os.path.exists(Paths.DOC_DIR):
                os.makedirs(Paths.DOC_DIR)
            if not os.path.exists(Paths.TXT_DIR):
                os.makedirs(Paths.TXT_DIR)
            if not os.path.exists(Paths.CHK_DIR):
                os.makedirs(Paths.CHK_DIR)
            if not os.path.exists(Paths.URL_DIR):
                os.makedirs(Paths.URL_DIR)

            headers = {'Content-Type': 'application/json; charset=utf-8'}
            r = requests.post(Urls.CLR_URL, headers=headers,
                              json={'name': st.session_state["username"]})
            # timed_alert(r.json()['message'])

    timed_alert('✅ Cleared all documents', type_='success')


if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False

if st.session_state['authentication_status']:
    st.markdown('## Manage your documents')
    st.markdown("---")

    c1, c2, c3 = st.columns([1, 1, 7])
    with c1:
        st.markdown('Documents: <span style="color:Teal">' +
                    f'{len(os.listdir(Paths.DOC_DIR))}</span>', unsafe_allow_html=True)

    with c2:
        st.markdown('Passages: <span style="color:Teal">' +
                    f'{len(os.listdir(Paths.CHK_DIR))}</span>', unsafe_allow_html=True)
    btn_container = st.empty()
    with btn_container:
        btn_clear = st.button('❌ Clear Document Store', on_click=clear_docs)
else:
    st.markdown('Please <a href="/" target="_self">login</a> to access this page',
                unsafe_allow_html=True)

