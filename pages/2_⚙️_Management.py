import os
import shutil
from glob import glob
import time

import streamlit as st

from config import Paths


def clear_docs():
    btn_container.empty()
    with progress_container:
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

    progress_container.empty()
    with progress_container:
        st.write('✔️ Cleared all documents')
        time.sleep(3)

    progress_container.empty()



btn_container = st.empty()
progress_container = st.empty()
with btn_container:
    btn_clear = st.button('❌ Clear Document Store', on_click=clear_docs)
