@ECHO OFF

::set the codepage to UTF-8 
chcp 65001 >NUL

CALL conda activate deploy
streamlit run "🤖_Doc._Chat.py"
PAUSE