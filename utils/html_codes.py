###---- Hide Streamlit menu and footer ----
HIDE_ST = """
        <style>
        #MainMenu {visibility: visible;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .viewerBadge_container__1QSob{visibility: hidden;}
        </style>
        """

###---- Hide contents of the sidebar ----
HIDE_BAR = """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:hidden;
    }
    </style>
"""

###---- Show contents of the sidebar ----
SHOW_BAR = """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:visible;
        width: 100%;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:visible;
    }
    </style>
"""

###---- Custom notification box style ----
NOTIF_STYLE = {'material-icons': {'color': 'lightgreen'},
               'text-icon-link-close-container': {'box-shadow': '#3896de 1px 1px 1px 1px',
                                                  'width': '90%',
                                                  'justify-content': 'space-between',
                                                  'align-content': 'left'},
               'notification-icon-container': {'padding': '5px'},
               'notification-text': {'color': 'lightblue',
                                     'font-family': '"Source Sans Pro", sans-serif',
                                     'font-size': '16px'},
               'close-button': {'padding': '5px'},
               'link': {'': ''}}
