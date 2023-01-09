import os
import yaml
import time
from functools import partial
import streamlit as st
from utils import timed_alert
import streamlit_authenticator as stauth
import requests


class UserDocs:
    def __init__(self):
        self.docs = {}
        self.paths = []

    def file_exists(self, file_name):
        found = False
        for doc in self.docs.values():
            if 'name' in doc.keys() and doc['name'] == file_name:
                found = True
        return found

    def add_doc(self, file_name, file_type):
        if self.file_exists(file_name):
            return False
        doc_id = os.urandom(8).hex()
        self.docs[doc_id] = {'name': file_name, 'type': file_type}
        return True
    
    def check_removed(self, curr_files):
        removed_files = []
        uploaded_names = [d[0] for d in curr_files]
        for doc_id, doc in self.docs.items():
            if 'name' in doc.keys() and doc['name'] not in uploaded_names:
                removed_files.append(n)
                del self.docs[doc_id]
        return removed_files
    
    def add_path(self, saved_path):
        self.paths.append(saved_path)


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
            st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
            authenticator.logout('Logout', 'sidebar')
            st.title('Intelligent Document Retrieval')
            st.text_input("Enter your question", value="")
            st.button('Answer', on_click=partial(send_question_to_api, None))
            return True

        elif st.session_state['authentication_status'] == False:
            st.error('Username/password is incorrect')
        elif st.session_state['authentication_status'] == None:
            st.warning('Please enter your username and password')
        
        return False
    
def send_question_to_api(question):
    timed_alert(f"Generating answer ...\n Please wait")

def send_link_to_api(link):
    timed_alert(f"Processing URL ...\n Please wait")

def upload_link():
    url = st.sidebar.text_input("Enter a url to crawl", value="")
    if url is not None or url != '':
        print('URL:', url)
        # st.sidebar.button('Crawl', on_click=partial(send_link_to_api, None))

def upload_doc(user_docs):
    uploaded_any = False
    uploaded_files = st.sidebar.file_uploader("Please choose a document file to upload",
                                            type=['txt', 'doc', 'docx', 'pdf'],
                                            accept_multiple_files=True)

    curr_files = []
    for file in uploaded_files:
        ## TODO: keep track of the uploaded files, then check if any file removed, then delete it from docs
        ## TODO: check if file saved or not, save if not exists
        if file is not None:
            curr_files.append((file.name, file.type))

            # # Hide filename on UI
            # css = """
            #     .uploadedFile {
            #         display: none;
            #     } """
            # st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
            # # Show uploaded file's info
            # file_details = {"FileName":file.name, "FileType":file.type}
            # st.write(file_details)
        
    for name_, type_ in curr_files:
        if user_docs.add_doc(name_, type_):
            save_path = save_uploaded_file(file)
            user_docs.add_path(save_path)
            uploaded_any = True
    if uploaded_any:
        timed_alert('Uploaded Successfully!')
    else:
        removed_names = user_docs.check_removed(curr_files)
        for n in removed_names:
            delete_file(n)
            timed_alert(f'Removed {n}')
    return uploaded_any


def delete_file(file_name):
    docs_dir = os.path.join('docs', st.session_state["username"])
    file_path = os.path.join(docs_dir, file_name)
    if not os.path.exists(file_path):
        os.delete(file_path)


def save_uploaded_file(uploaded_file):
    docs_dir = os.path.join('docs', st.session_state["username"])
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    save_path = os.path.join(docs_dir, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

def send_to_api(user_docs):
    # placeholder = st.sidebar.empty()
    # placeholder.success(f"Started processing {user_docs.paths[0]}")
    st.sidebar.success(f"Started processing ...\n Please wait")

if auth():
    # TODO: upload_doc: only uploads and returns list of uploaded_files
    # TODO: submit_docs: check if new/exists and save + proper messages + clear uploaded list
    user_docs = UserDocs()
    upload_link()
    # upload_doc(user_docs)
    if upload_doc(user_docs):
        st.sidebar.button('Process', on_click=partial(send_to_api, user_docs))