import requests
import pandas as pd

# get data from api and store it in a dataframe
url = 'https://api.covid19india.org/data.json'
req = requests.get(url)
dict_req = req.json()
df_in_daily = pd.DataFrame(dict_req['cases_time_series'])


def get_in_df():
    """
    creates dataframe for India containing require parameters
    :return: structured dataframe for India
    """
    df_in_daily['date'] = df_in_daily['date'] + '2020'
    df_in_daily['date'] = pd.to_datetime(df_in_daily['date'])
    df_in_daily['dailyconfirmed'] = pd.to_numeric(df_in_daily['dailyconfirmed'])
    df_in_daily['dailyrecovered'] = pd.to_numeric(df_in_daily['dailyrecovered'])
    df_in_daily['dailydeceased'] = pd.to_numeric(df_in_daily['dailydeceased'])
    df_in_daily['cum_confirmed'] = df_in_daily['dailyconfirmed'].cumsum()
    df_in_daily['active'] = df_in_daily['cum_confirmed'] - (
            df_in_daily['dailyrecovered'].cumsum() + df_in_daily['dailydeceased'].cumsum())
    return df_in_daily
