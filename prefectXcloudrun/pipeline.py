import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import requests
import datetime
from datetime import timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.common.exceptions import TimeoutException

from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}

driver = webdriver.Chrome(options=chrome_options)

##########################################################################
#Extracting the Data From Yahoo Finace
@task(log_prints=True, tags=["extract"])
def capture_data(url: str) -> pd.DataFrame:
    
    """This function is used to extract data from Yahoo Finance"""
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    name = []
    price = []
    market_cap =[]
    
    #using the html tags, we can identify where the data is located and then
    #scrape that data
    for content in soup.findAll('td', attrs={'aria-label':"Symbol"}):
        name.append(content.text)
        
    for content in soup.findAll('td', attrs={'aria-label':"Price (Intraday)"}):
        price.append(content.text.replace(',',''))
        
    for content in soup.findAll('td', attrs={'aria-label':"Market Cap"}):
        market_cap.append(content.text)
        
        
    df = pd.DataFrame({'name':name, 'price':price, 'market_cap':market_cap})

    return df

#Transforming the Data
@task(log_prints=True, tags=['Transform'])  
def trans_df(df: pd.DataFrame) -> pd.DataFrame:

    current_time = datetime.datetime.now()
    current_timestamp = pd.Timestamp(current_time.strftime('%Y-%m-%d %H:%M'))

    df['date'] = current_timestamp

    #some basic data cleaning steps to ensure the data comes out in the right format
    df['date'] = df['date'].astype('str')
    
    df['price'] = pd.to_numeric(df['price'])
    
    for i in range(len(df['market_cap'])):
        if df['market_cap'][i][-1]=='B':
            df['market_cap'][i] = df['market_cap'][i].replace('B','')
            df['market_cap'][i] = pd.to_numeric(df['market_cap'][i]) * 1000000
        elif str(df['market_cap'][i][-1])=='M':
            df['market_cap'][i] = df['market_cap'][i].replace('M','')
            df['market_cap'][i] = pd.to_numeric(df['market_cap'][i]) * 1000            
        else:
            df['market_cap'][i] = df['market_cap'][i].replace(',','')
            
    df['market_cap'] = pd.to_numeric(df['market_cap'])
          
    df = df[['date','name','price','market_cap']]
    
    return df

#Loading the Data 
@task(log_prints=True, tags=['Load'])
def batch(df: pd.DataFrame, tablename: str) -> None:
    
    connection_block = SqlAlchemyConnector.load("postgres-connector")
    with connection_block.get_connection(begin=False) as engine:

        df.to_sql(name=tablename, con=engine, if_exists='append')

        print('Batch Successful')

        engine.connect().close()

@flow(name='Flow-Postgres-ETL')
def main(url: str, tablename: str):

    url = url

    tablename = tablename

    data = capture_data(url)

    df = trans_df(data)

    batch(df, tablename)

if __name__ == '__main__':

    url = 'https://finance.yahoo.com/crypto/?.tsrc=fin-srch&offset=0&count=15'

    tablename = 'batchpg1'

    main(url, tablename)
    
    
