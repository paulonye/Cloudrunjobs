import os
from scrape import capture_data
from connect import get_connect_sheet
from connect import push_to_sheets
from connect import append_new_data
import argparse
import pandas as pd


def run_job():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--googlesheet',
        dest='googlesheet',
        required=False,
        type=str,
        help='The name of the Google Sheet'

    )

    parser.add_argument(
        '--sheetname',
        dest='sheetname',
        required=False,
        type=str,
        help='The name of the worksheet'
    )

    known_args = parser.parse_args()

    google_sheet_name = known_args.googlesheet
    sheet_name = known_args.sheetname

    #Running the Pipeline 
    #This scrapes the data from Yahoo Finance
    data = capture_data()
    
    #This imports the service account credentials that will allow us access the sheet
    client = get_connect_sheet()
    
    #Once the connection has been made, the Google Sheet can now be accessed
    push_sheet=client.open(google_sheet_name)
    #opening the data sheet
    data_push=push_sheet.worksheet(sheet_name)
    data_push_df=pd.DataFrame.from_dict(data_push.get_all_records())


    if len(data_push_df) == 0:
        push_to_sheets(data_push, data)
    else:
        append_new_data(data, sheet_name, google_sheet_name)

if __name__ == '__main__':
    try:
        run_job()
    except Exception as e:
        print(e)
        os._exit(0)

