import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import requests
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.common.exceptions import TimeoutException

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}

driver = webdriver.Chrome(options=chrome_options)

#########################################
# options = Options()
# options.headless = True

# driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)


##########################################################################

def capture_data():
    
    """This function is used to capture the data from Yahoo Finance"""
    
    url = 'https://finance.yahoo.com/crypto/?.tsrc=fin-srch&offset=0&count=15'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    #this prints out the current timestamp of your machine at the time the data was captured
    #you should note that since we are using a remote machine, there will be time differences
    #for me, based on the time I selected, my local time(WAT) is one hour ahead
    current_time = datetime.datetime.now()
    current_timestamp = pd.Timestamp(current_time.strftime('%Y-%m-%d %H:%M'))
    
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

if __name__ == '__main__':
    print(capture_data())
    
