import pandas as pd

# get data from csv and store it in a dataframe
df_all_districts = pd.read_csv('https://api.covid19india.org/csv/latest/districts.csv')


# get dataframe for a district containing required parameters
def get_district_df(district):
    df_district = df_all_districts[df_all_districts['District'] == district]
    df_district['Confirmed'] = pd.to_numeric(df_district['Confirmed'])
    df_district['Recovered'] = pd.to_numeric(df_district['Recovered'])
    df_district['Deceased'] = pd.to_numeric(df_district['Deceased'])
    df_district['Active'] = df_district['Confirmed'] - (df_district['Recovered'] + df_district['Deceased'])
    df_district = df_district.assign(New=df_district['Confirmed'].diff().fillna(df_district['Confirmed']).values)
    df_district['New'] = pd.to_numeric(df_district['New'])
    df_district['Date'] = pd.to_datetime(df_district['Date'])
    df_district = df_district[1:-1]
    df_district = df_district.reset_index(drop=True)
    return df_district


districts = list(df_all_districts['District'].unique())
districts.remove("Unknown")
districts.remove("Others")
