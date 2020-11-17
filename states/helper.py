import requests
import json
import pandas as pd

# state codes, since Covid 19 state time series data has states codes
state_codes = ["an", "ap", "ar", "as", "br", "ch", "ct", "dd", "dl", "dn", "ga", "gj", "hp", "hr", "jh", "jk", "ka",
               "kl", "la", "ld", "mh", "ml",
               "mn", "mp", "mz", "nl", "or", "pb", "py", "rj", "sk", "tg", "tn", "tr", "tt", "un", "up", "ut", "wb"]

# dictionary to map state names to state codes
state_code_dict = {'Maharashtra': 'mh', 'Gujrat': 'gj', 'Goa': 'ga', 'Tamil Nadu': 'tn', 'Punjab': 'pb',
                   'Rajasthan': 'rj', 'Madhya Pradesh': 'mp', 'Uttar Pradesh': 'up',
                   'Bihar': 'br', 'West Bengal': 'wb', 'Karnataka': 'ka', 'Kerala': 'kl', 'Odisha': 'or',
                   'Jharkhand': 'jh', 'Jammu and Kashmir': 'jk', 'Haryana': 'hr', 'Delhi': 'dl',
                   'Himachal Pradesh': 'hp', 'Sikkim': 'sk', 'Assam': 'as', 'Chhattisgarh': 'ct',
                   'Andhra Pradesh': 'ap', 'Arunachal Pradesh': 'ar', 'Manipur': 'mn', 'Meghalaya': 'ml',
                   'Mizoram': 'mz', 'Nagaland': 'nl', 'Telangana': 'tg', 'Tripura': 'tr', 'Uttarakhand': 'ut',
                   'Ladakh': 'la', 'Andaman and Nicobar Islands': 'an', 'Lakshadweep': 'ld',
                   'Puducherry': 'py'}

# dictionary to map state codes to state names
reverse_state_code_dict = {v: k for k, v in state_code_dict.items()}

# get data from api and store it in dataframe
url = 'https://api.covid19india.org/states_daily.json'
req = requests.get(url)
dict_req = req.json()
df_all_states = pd.DataFrame(dict_req['states_daily'])
df_all_states['date'] = pd.to_datetime(df_all_states['date'])


# get daily confirmed, recovered and deceased cases for a state
def get_confirmed_recovered_deceased(df, state):
    con = df[df['status'] == 'Confirmed'][['date', state]]
    con.columns = ['date', 'confirmed']
    rec = df[df['status'] == 'Recovered'][['date', state]]
    rec.columns = ['date1', 'recovered']
    dec = df[df['status'] == 'Deceased'][['date', state]]
    dec.columns = ['date1', 'deceased']
    return con, rec, dec


# get dataframe for a state containing required parameters
def get_state_df(state_code):
    df_state = df_all_states[['date', state_code, 'status']].copy()
    con, rec, dec = get_confirmed_recovered_deceased(df_state, state_code)
    df_state_daily = pd.concat([con.reset_index(drop=True), rec.reset_index(drop=True), dec.reset_index(drop=True)],
                               axis=1)
    df_state_daily = df_state_daily[['date', 'confirmed', 'recovered', 'deceased']].copy()
    df_state_daily['confirmed'] = pd.to_numeric(df_state_daily['confirmed'])
    df_state_daily['recovered'] = pd.to_numeric(df_state_daily['recovered'])
    df_state_daily['deceased'] = pd.to_numeric(df_state_daily['deceased'])
    df_state_daily['cum_confirmed'] = df_state_daily['confirmed'].cumsum()
    df_state_daily['active'] = df_state_daily['cum_confirmed'] - (
            df_state_daily['recovered'].cumsum() + df_state_daily['deceased'].cumsum())
    return df_state_daily
