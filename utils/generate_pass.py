import pickle

import streamlit_authenticator as stauth

# usernames = ["farhad", "saeed"]
passwords = ["123", "456"]

hashed_passwords = stauth.Hasher(passwords).generate()

with open("hashed_pw.pkl", "wb") as f:
    pickle.dump(hashed_passwords, f)
