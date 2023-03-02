import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import requests
import datetime
from pathlib import Path
from datetime import timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.common.exceptions import TimeoutException

from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

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

    print(len(df))

    return df

#Transforming the Data
@task(log_prints=True, tags=['Transform'])  
def trans_df(df: pd.DataFrame) -> Path:

    current_time = datetime.datetime.now()
    current_date = pd.Timestamp(current_time.strftime('%Y-%m-%d')).date()

    df['date'] = current_date

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

    path = Path(f"data/yahoo-{current_date}.csv")

    df.to_csv(path)
    
    return path

#Loading the Data to Google Cloud Storage
@task(log_prints=True, tags=["load to Cloud Storage"])
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return


@flow(name='Flow-CloudStorage-EL')
def main(url: str):

    data = capture_data(url)

    df = trans_df(data)

    write_gcs(df)

if __name__ == '__main__':

    url = 'https://finance.yahoo.com/crypto/?.tsrc=fin-srch&offset=0&count=100'

    main(url)
    
    
