import pandas as pd
import numpy as np
import yfinance as yf

# FF3 data
def load_ff3(filepath_1=None):
    """load the Fama-French 3 factors from a csv file"""
    #filepath_1 = '/Users/nkeniryanbonny/Desktop/projet_fama_french/data:work:/fama_f3_work.csv'

    data = pd.read_csv(filepath_1, sep=',', skiprows=6, engine='python') 

    data.rename(columns={data.columns[0]: 'Date'}, inplace=True)
    data.columns = data.columns.str.strip()

    data['Date'] = data['Date'].astype(str)
    data = data[data['Date'].str.len() == 8]
    data = data[data['Date'].str.isdigit()]

    data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d', errors='coerce') 
    data.set_index('Date', inplace=True)
    data = data.dropna()
    return data

# FF5 data
def load_ff5(filepath_2=None):
    """load the Fama-French 5 factors from a csv file"""
    #filepath_2 = '/Users/nkeniryanbonny/Desktop/projet_fama_french/data:work:/ff5_daily_work.csv'

    data_n = pd.read_csv(filepath_2, sep=',', skiprows=6, engine='python') # engine moteur de parsing

    data_n.rename(columns={data_n.columns[0]: 'Date'}, inplace=True)
    data_n.columns = data_n.columns.str.strip()

    data_n['Date'] = data_n['Date'].astype(str)
    data_n = data_n[data_n['Date'].str.len() == 8]
    data_n = data_n[data_n['Date'].str.isdigit()]

    data_n['Date'] = pd.to_datetime(data_n['Date'], format='%Y%m%d', errors='coerce') 
    data_n.set_index('Date', inplace=True)
    return data_n

# ORCL data
def load_oracle_prices(data, data_n):
    orcl = yf.download('ORCL', start='2016-01-01', end='2025-07-31', progress=False)
    orcl_price = pd.DataFrame({
        'orcl_price': orcl['Close'].squeeze()  # squeeze() enlève les dimensions inutiles
    }, index=orcl.index)
    merged_data = data.join(orcl_price, how='inner')
    merged_data['daily_orcl_returns'] = merged_data.orcl_price.pct_change() * 100
    data = merged_data.dropna()
    data['orcl_excess_returns'] = data['daily_orcl_returns'] - data['RF']

    data_new = data_n.join(data['orcl_excess_returns'], how='inner')

    return data, data_new

# --------- Calculate oracle excess returns --------------
# calculate oracle daily returns 
