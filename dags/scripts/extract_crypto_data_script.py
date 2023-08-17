from sqlalchemy import create_engine
from binance.client import Client
from dotenv import load_dotenv
import pandas as pd
import datetime 
import os


#load env variables from .env file
load_dotenv('../../.env')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

binance_client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)


def connect_postgress():
    con_string = os.getenv('CON_STRING')
    engine = create_engine(con_string)

    return engine.connect()


def get_binance_symbols():
    symbols = binance_client.get_exchange_info()
    list_symbols = [symbol['symbol'] for symbol in symbols['symbols'] if symbol['symbol'].endswith('EUR')]

    return(list_symbols)

def get_previous_timestamp():
    con = connect_postgress()
    prev_timestamp = con.execute('''select max(close_time) from postgres.public.crypto_prices''').fetchall()
    con.close()
    prev_timestamp = prev_timestamp[0][0]
    if not prev_timestamp:
        print('no prev records were found')
        prev_timestamp = datetime.datetime.today() - datetime.timedelta(hours=1)
    
    print('fuuuck')
    print(prev_timestamp)
  
    return  prev_timestamp.strftime("%d %b %Y %H:%M:%S")

def get_max_timestamp():
    binance_client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)
    max_time_ms = binance_client.get_klines(symbol='BTCUSDT', interval='5m')[-2][0]
    max_timestamp = datetime.datetime.fromtimestamp(max_time_ms/1000)

    return max_timestamp.strftime("%d %b %Y %H:%M:%S")

def pull_data():
    cryptos = get_binance_symbols()
    prev_timestamp = get_previous_timestamp()
    max_timestamp = get_max_timestamp()
    df_list = []
    for crypto in cryptos:
        klines = binance_client.get_historical_klines(crypto, '5m', prev_timestamp, max_timestamp) 
        data = pd.DataFrame(klines, columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    
        data['crypto'] = crypto
        df_list.append(data)

    data_final = pd.concat(df_list)
    return data_final


def clean_data():
    data = pull_data()
    #drop ignore column
    data.drop(['ignore'], inplace=True, axis=1)
    data.loc[:, 'open_time'] = data.open_time.apply(lambda x: datetime.datetime.fromtimestamp(x/1000))
    data.loc[:, 'close_time'] = data.close_time.apply(lambda x: datetime.datetime.fromtimestamp(x/1000))

    #convert ms time to timestamp
    data['open_time']=data['open_time'].values.astype('datetime64[s]')
    data['close_time']=data['close_time'].values.astype('datetime64[s]')

    # change data types
    data['open_time']=data['open_time'].values.astype('datetime64[s]')
    data['close_time']=data['close_time'].values.astype('datetime64[s]')
    data["open"] = data["open"].astype(float)
    data["high"] = data["high"].astype(float)
    data["low"] = data["low"].astype(float)
    data["close"] = data["close"].astype(float)
    data["volume"] = data["volume"].astype(float)
    data["quote_av"] = data["quote_av"].astype(float)
    data["tb_base_av"] = data["tb_base_av"].astype(float)
    data["tb_quote_av"] = data["tb_quote_av"].astype(float)

    return data

def load_to_postgres():
    con = connect_postgress()
    data = clean_data()  
    data.to_sql('crypto_prices', con=con, if_exists='append',
          index=False)
prev_timestamp = datetime.datetime.today() - datetime.timedelta(hours=1)
