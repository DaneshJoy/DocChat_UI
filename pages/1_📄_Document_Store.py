import os
import shutil
import requests
from random import randint
from functools import partial
import base64


import streamlit as st
import streamlit_authenticator as stauth
from streamlit_custom_notification_box import custom_notification_box
from st_clickable_images import clickable_images
from haystack.nodes import Crawler
from haystack.nodes import PDFToTextConverter
from haystack.utils import convert_files_to_docs, clean_wiki_text
from haystack.nodes import PreProcessor

from utils import timed_alert


TMP_DIR = os.path.join(os.getcwd(), 'temp', st.session_state["username"])
DOC_DIR = os.path.join(os.getcwd(), 'docs', st.session_state["username"])
TXT_DIR = os.path.join(os.getcwd(), 'txts', st.session_state["username"])
CHK_DIR = os.path.join(os.getcwd(), 'chks', st.session_state["username"])
URL_DIR = os.path.join(os.getcwd(), 'urls', st.session_state["username"])

preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=False,
    split_by="word",
    split_length=200,
    split_overlap=50,
    split_respect_sentence_boundary=True,
)

styles = {'material-icons':{'color': 'lightgreen'},
          'text-icon-link-close-container': {'box-shadow': '#3896de 1px 1px 1px 1px',
                                             'width': '90%',
                                             'justify-content': 'space-between',
                                             'align-content': 'left'},
          'notification-icon-container': {'padding': '5px'},
          'notification-text': {'color': 'lightblue',
                                'font-family': '"Source Sans Pro", sans-serif',
                                'font-size': '16px'},
          'close-button':{'padding': '5px'},
          'link':{'':''}}

# # Icons from https://fonts.google.com/icons
# # with st.sidebar:
# custom_notification_box(icon='add_task', textDisplay='Finished processing documents',
#                         externalLink='', url='#', styles=styles, key="foo")
# custom_notification_box(icon='info', textDisplay='Duplicate files: ',
#                         externalLink='', url='#', styles=styles, key="foo2")


images = []
for file in ["assets/delete.png", "assets/download.png"]:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        images.append(f"data:image/png;base64,{encoded}")


class UserDocs:
    def __init__(self):
        pass

    def file_exists(self, file_name):
        existing_files = os.listdir(DOC_DIR)
        temp_files = os.listdir(TMP_DIR)
        for doc in [*existing_files, *temp_files]:
            if doc == file_name:
                return True
        return False
    
    def check_removed(self, all_files):
        removed_files = []
        
        existing_names = os.listdir(DOC_DIR)
        for doc_file in existing_names:
            if doc_file not in all_files:
                removed_files.append(doc_file)
        return removed_files


def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def upload_link():
    url = st.sidebar.text_input("Enter a url to crawl", value="")
    if url is not None or url != '':
        st.sidebar.markdown(f"{url}")
        # st.sidebar.button('Crawl', on_click=partial(send_link_to_api, None))
    
    
    # from selenium import webdriver
    # options = webdriver.ChromeOptions()
    # or from selenium.webdriver.chrome.options import Options
    # options.binary_location = '/home/appuser/.wdm/drivers/chromedriver/linux64/109.0.5414/chromedriver'
    if url != '':
        with progress_container:
            placeholder = st.empty()
            placeholder.write(' 🚧 >>> Processing URL ...')
        
        with st.spinner('Please wait ...'):
    
            crawler = Crawler(output_dir=URL_DIR, crawler_depth=1,
                webdriver_options=["--disable-gpu", "--no-sandbox", "--single-process"])
            sub_urls = crawler._extract_sublinks_from_url(base_url=url)
            # crawler._extract_sublinks_from_url -> already_found_links: Optional[List] = None
            st.sidebar.write(f"Found {len(sub_urls)} sub-urls")
            # for u in sub_urls:
            #     st.sidebar.markdown(f"{u}")
            
            placeholder.empty()

if 'key' not in st.session_state: st.session_state.key = str(randint(1000, 100000000))
def upload_doc(user_docs, uploaded_contents):
    uploaded_any = False
    uploaded_files = st.sidebar.file_uploader("Upload a document file",
                                            type=['txt', 'doc', 'docx', 'pdf'],
                                            accept_multiple_files=True,
                                            key=st.session_state.key)

    if uploaded_files:
        css = """
            .css-fis6aj {
                display: none;
            }"""
        st.sidebar.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

        with progress_container:
            placeholder = st.empty()
            placeholder.write(' 🚧 >>> Processing documents ...')
            process_progress = st.progress(0)
        for i, file in enumerate(uploaded_files):
            # file_details = {"FileName":file.name, "FileType":file.type}

            if not user_docs.file_exists(file.name):
                save_path = save_uploaded_file(file)
                uploaded_any = True
            else:
                with progress_container:
                    timed_alert(f'Uploaded file already exists:\n "{file.name}"',
                                type_='error')
            process_progress.progress((i+1) * 100//len(uploaded_files))
        
        all_docs = convert_files_to_docs(dir_path=TMP_DIR,
                                        clean_func=clean_wiki_text,
                                        split_paragraphs=True)
        for doc_txt in all_docs:
            doc_filename = f"{os.path.basename(doc_txt.meta['name']).split('.')[0]}.txt"
            with open(os.path.join(TXT_DIR, doc_filename), 'w', encoding="utf-8") as f:
                f.write(doc_txt.content)
        
        # %% Preprocess
        docs_default = preprocessor.process(all_docs)
        print(f"n_docs_input: {len(all_docs)}\nn_docs_output: {len(docs_default)}")

        for chunk in docs_default:
            chunk_filename = f"{chunk.meta['name']}_{chunk.meta['_split_id']}.txt"
            with open(os.path.join(CHK_DIR, chunk_filename), 'w', encoding="utf-8") as f:
                f.write(chunk.content)

        with progress_container:
            st.markdown(f"Successfully processed **{len(all_docs)}** document(s)"
                f"and created **{len(docs_default)}** passages")

        placeholder.empty()
        process_progress.empty()
        uploaded_files = None
        if 'key' in st.session_state.keys():
            st.session_state.pop('key')
        with progress_container:
            timed_alert('Document processing finished')
            # custom_notification_box(icon='add_task',
            #                     textDisplay='Finished processing documents',
            #                     externalLink='', url='#', styles=styles, key="foo")
        
        for f in os.listdir(TMP_DIR):
            shutil.move(os.path.join(TMP_DIR, f), os.path.join(DOC_DIR, f))

    return uploaded_any



def delete_file(file_name):
    file_path = os.path.join(DOC_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)


def save_uploaded_file(uploaded_file):
    save_path = os.path.join(TMP_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path


def card_buttons():
    return ("""
        <style>
        .button {
        border: none;
        color: navy;
        padding: 5px 5px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 12px;
        margin: 4px 2px;
        cursor: hand;
        }

        .button1 {color: red; background-color: #FFCCCC;}
        .button2 {background-color: lightblue;}
        </style>"""
        f'<button class="button button2">download</button>'
        f'<button class="button button1">delete</button>'
        
    )
    
def process_docs(user_docs):
    # Hide uploaded filenames on UI
    with st.spinner('Processing Documents ...'):
        css = """
            .css-fis6aj {
                display: none;
            }"""
        st.sidebar.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    

    # placeholder = st.sidebar.empty()
    # placeholder.success(f"Started processing {user_docs.paths[0]}")

    # del user_docs.docs

if 'authentication_status' not in st.session_state:
    st.session_state.authentication_status = False

if st.session_state['authentication_status']:    
    
    for _ in range(2):
        st.sidebar.write("")
    
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
    if not os.path.exists(DOC_DIR):
        os.makedirs(DOC_DIR)
    if not os.path.exists(TXT_DIR):
        os.makedirs(TXT_DIR)
    if not os.path.exists(CHK_DIR):
        os.makedirs(CHK_DIR)
    if not os.path.exists(URL_DIR):
        os.makedirs(URL_DIR)

    uploaded_contents = os.listdir(DOC_DIR)


    st.markdown('## Processed Documents')
    st.markdown("---")

    progress_container = st.container()

    # uploaded_names = [d['name'] for d in user_docs.docs.values()]
    # all_files = list(set([*uploaded_contents, *uploaded_names]))
    # removed_names = user_docs.check_removed(all_files)
    # if len(removed_names) > 0:
    #     for n in removed_names:
    #         delete_file(n)
    #         timed_alert(f'Removed {n}')

    cc = st.columns(2)
    for i, f in enumerate(uploaded_contents):
        with cc[i%2]:
            with st.expander(f"{f}", expanded=False):
                # html3 = f"""
                #     <div>
                #         <button type="button">delete</button>
                #         <button type="button">download</button>
                #     </div>

                #     """

                # # st.markdown(html3, unsafe_allow_html=True)
                # st.markdown(card_buttons(), unsafe_allow_html=True)
                # # st.button('delete', key=i)
                # # st.button('download', key=i+100)

                clicked = clickable_images(
                    images,
                    div_style={"display": "flex", "justify-content": "right", "flex-wrap": "wrap"},
                    img_style={"margin": "2px", "height": "30px", "cursor": "pointer"},
                    key=i
                )

                # st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")

    user_docs = UserDocs()
    
    
    # upload_doc(user_docs)
    uploaded = upload_doc(user_docs, uploaded_contents)



    if uploaded:
        st.experimental_rerun()
    #     btn = st.sidebar.button('Process', on_click=partial(process_docs, user_docs))
    
    #     if btn and 'key' in st.session_state.keys():
    #         st.session_state.pop('key')
    #         st.experimental_rerun()

    st.sidebar.markdown("---")

    upload_link()

    st.sidebar.markdown("---")
    
    
    
    

else:
    st.markdown('Please [login](/) to access your documents')