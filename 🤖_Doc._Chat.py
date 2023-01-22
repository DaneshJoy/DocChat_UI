import os
import requests
from functools import partial

import streamlit as st
import streamlit_authenticator as stauth
import openai

from utils.utils import auth
from utils.utils import timed_alert
from utils.html_codes import *
from utils.api import send_question_to_api
from utils.utils import set_state_if_absent


st.set_page_config(page_title="Doc. Chat", page_icon="🤖", layout="wide",
                   menu_items={'About': "### Doc. Chat app!"})

st.markdown(HIDE_ST, unsafe_allow_html=True)

COMPLETIONS_MODEL = "text-davinci-003"
COMPLETIONS_API_PARAMS = {
    "temperature": 0.0,
    "max_tokens": 300,
    "model": COMPLETIONS_MODEL,
}

openai.api_key = os.getenv("OPENAI_API_KEY")
header = """Answer the question as truthfully as possible using the provided context, \
and include the parts of the context that are used to generate the answer after the answer starting with "\nRef:", \
and if the answer is not contained within the text below, say "I don't know."\n\nContext:\n"""

def logout(authenticator):
    for _ in range(15):
        st.sidebar.write("")
    st.sidebar.markdown('---')
    st.sidebar.write(f'Logged in as "*{st.session_state["name"]}*"')
    authenticator.logout('Logout', 'sidebar')

def new_question():
    st.session_state.new_question = True

def main():
    set_state_if_absent(new_question, False)
    authenticator = auth()
    if authenticator:
        st.markdown(SHOW_BAR, unsafe_allow_html=True)
        # set_state_if_absent('question', None)

        st.title('Doc. Chat')
        st.markdown("##### Intelligent Question-Answering on Documents")
        # st.markdown('---')
        st.text_input(label="Query", value="", placeholder="Enter your question",
                      key="question", label_visibility='hidden', on_change=new_question)
        clicked = st.button('Answer', on_click=new_question)
        if clicked and not st.session_state.new_question:
            with st.spinner('Please wait...'):
                headers = {'Content-Type': 'application/json; charset=utf-8'}
                r = requests.post(f"http://54.242.28.52/doc/get_related_contents",
                                  headers=headers,
                                  json={'name': st.session_state["username"],
                                        'question': st.session_state.question})
                if 'error' in r.text.lower():
                    st.write('Answer: Not Found !')
                else:
                    res = r.json()
                    refs = [d['content'] for d in res['documents']]
                    chosen_sections = '\n'.join(refs)
                    prompt = header + "".join(chosen_sections) + "\n\n Q: " + st.session_state.question + "\n A:"
                    response = openai.Completion.create(prompt=prompt, **COMPLETIONS_API_PARAMS)
                    full_ans = response["choices"][0]["text"].strip(" \n")
                    if "Ref:" in full_ans:
                        st.write('Answer:\n', full_ans.split('Ref:')[0])
                        ref_ = full_ans.split('Ref:')[1].strip()
                        st.markdown(f'Reference:\n "*{ref_}*"')
                    else:
                        st.write('Answer:\n', full_ans)
                    with st.expander('Related Contents', expanded=False):
                        for d in res['documents']:
                            st.write(d)
            st.session_state.new_question = False

        logout(authenticator)
    else:
        st.markdown(HIDE_BAR, unsafe_allow_html=True)


main()
