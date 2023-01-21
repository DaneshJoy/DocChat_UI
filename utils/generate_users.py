import yaml
import pickle

import streamlit_authenticator as stauth

with open("hashed_pw.pkl", "rb") as f:
    hashed_passwords = pickle.load(f)

creds = {'credentials':
         {'usernames':
          {'farhad':
           {'email': 'farhad@visioimpulse.com',
            'name': 'Farhad',
            'password': hashed_passwords[0]},
           'saeed':
           {'email': 'saeed.discovery@gmail.com',
            'name': 'Saeed',
            'password': hashed_passwords[1]},
           'guest':
           {'email': '',
            'name': 'Guest',
            'password': hashed_passwords[2]}
           }
          },
         'cookie':
             {'expiry_days': 30,
              'key': '123456789',
              'name': 'auth'},
         'preauthorized':
             {'emails': ['saeed.discovery@gmail.com',
                         'farhad@visioimpulse.com']}
         }


with open("creds.yaml", "w") as f:
    yaml.dump(creds, f)
