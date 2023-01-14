import os
import shutil
import time
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
from config import Paths



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


download_image = []
for file in ["assets/download.png"]:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        download_image.append(f"data:image/png;base64,{encoded}")

delete_image = []
for file in ["assets/delete.png"]:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        delete_image.append(f"data:image/png;base64,{encoded}")


class UserDocs:
    def __init__(self):
        pass

    def file_exists(self, file_name):
        existing_files = os.listdir(Paths.DOC_DIR)
        temp_files = os.listdir(Paths.TMP_DIR)
        for doc in [*existing_files, *temp_files]:
            if doc == file_name:
                return True
        return False
    
    def check_removed(self, all_files):
        removed_files = []
        
        existing_names = os.listdir(Paths.DOC_DIR)
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
            # webdriver_options=["--disable-gpu", "--no-sandbox", "--single-process"])
            crawler = Crawler(output_dir=Paths.URL_DIR, crawler_depth=1)
            sub_urls = crawler._extract_sublinks_from_url(base_url=url)
            # crawler._extract_sublinks_from_url -> already_found_links: Optional[List] = None
            st.sidebar.write(f"Found {len(sub_urls)} sub-urls")
            # for u in sub_urls:
            #     st.sidebar.markdown(f"{u}")
            
            placeholder.empty()

def preocess_docs():
    all_docs = convert_files_to_docs(dir_path=Paths.TMP_DIR,
                                    clean_func=clean_wiki_text,
                                    split_paragraphs=True)
    for doc_txt in all_docs:
        doc_filename = f"{os.path.basename(doc_txt.meta['name']).split('.')[0]}.txt"
        with open(os.path.join(Paths.TXT_DIR, doc_filename), 'w', encoding="utf-8") as f:
            f.write(doc_txt.content)
    
    # %% Preprocess
    chunks = preprocessor.process(all_docs)
    print(f"n_docs_input: {len(all_docs)}\nn_docs_output: {len(chunks)}")

    for chunk in chunks:
        chunk_filename = f"{chunk.meta['name']}_{chunk.meta['_split_id']}.txt"
        with open(os.path.join(Paths.CHK_DIR, chunk_filename), 'w', encoding="utf-8") as f:
            f.write(chunk.content)
    
    return len(all_docs), len(chunks)


if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = str(randint(1000, 100000000))
def upload_doc(user_docs, uploaded_contents):
    uploaded_any = False
    uploaded_files = st.sidebar.file_uploader("📤 Upload a document file",
                                            type=['txt', 'doc', 'docx', 'pdf'],
                                            accept_multiple_files=True,
                                            key=st.session_state.uploader_key)

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
            elif not uploaded_any:
                with progress_container:
                    timed_alert(f'Uploaded file already exists:\n "{file.name}"',
                                type_='error')
                    
            process_progress.progress((i+1) * 100//len(uploaded_files))
        
        num_docs, num_chunks = preocess_docs()

        with progress_container:
            if num_docs > 0:
                message = (f"Processed {num_docs} document(s)"
                        f"and created {num_chunks} passages")
                
                custom_notification_box(icon='add_task',
                                    textDisplay=message,
                                    externalLink='', url='#', styles=styles, key="foo")
                time.sleep(2)

        placeholder.empty()
        process_progress.empty()
        uploaded_files = None
        if 'uploader_key' in st.session_state.keys():
            st.session_state.pop('uploader_key')
        # with progress_container:
        #     timed_alert('Document processing finished')
        
        for f in os.listdir(Paths.TMP_DIR):
            shutil.move(os.path.join(Paths.TMP_DIR, f), os.path.join(Paths.DOC_DIR, f))

    return uploaded_any



def delete_file(file_name):
    file_path = os.path.join(Paths.DOC_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)


def save_uploaded_file(uploaded_file):
    save_path = os.path.join(Paths.TMP_DIR, uploaded_file.name)
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

    uploaded_contents = os.listdir(Paths.DOC_DIR)


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
    st.session_state['prep'] = False

    if not st.session_state['prep'] :
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

                    # clicked0 = clickable_images(
                    #     download_image,
                    #     div_style={"display": "flex", "justify-content": "right", "flex-wrap": "wrap"},
                    #     img_style={"margin": "2px", "height": "30px", "cursor": "pointer"},
                    #     key=f"download_{i}"
                    # )

                    # clicked1 = clickable_images(
                    #     delete_image,
                    #     div_style={"display": "flex", "justify-content": "right", "flex-wrap": "wrap"},
                    #     img_style={"margin": "2px", "height": "30px", "cursor": "pointer"},
                    #     key=f'delete_{i}'
                    # )

                    with open(os.path.join(Paths.DOC_DIR, f), "rb") as file:
                        btn = st.download_button(
                                label="⬇️ Download PDF",
                                data=file,
                                file_name=f,
                                mime='application/octet-stream',
                                key=f'd_pdf_{i}'
                            )
                    
                    # # pdf from string
                    # import pdfkit
                    # pdf = pdfkit.from_string(html, False)
                    
                    # txt_file = f.split('.')[0] + '.txt'
                    # with open(os.path.join(Paths.TXT_DIR, txt_file), "rb") as file:
                    #     btn = st.download_button(
                    #             label="Download Text",
                    #             data=file,
                    #             file_name=txt_file,
                    #             mime='text/plain',
                    #             key=f'd_txt_{i}'
                    #         )
    

                    # print(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")
        st.session_state['prep'] = True

    user_docs = UserDocs()

    # print(st.session_state)

    # if st.session_state.get("delete_0") is not None:
    #     print('---------------')
    
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