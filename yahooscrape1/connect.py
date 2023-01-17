"""This python file sets up a secured connection
    to the script"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import df2gspread as d2g
from gspread_dataframe import set_with_dataframe
import os
key_file = os.getenv('key_file')

# defining the scope of the application
scope_app = ['https://www.googleapis.com/auth/drive',
             'https://spreadsheets.google.com/feeds']


def get_connect_sheet():

    cred = ServiceAccountCredentials.from_json_keyfile_name(
        key_file, scope_app)

    client = gspread.authorize(cred)

    return client

def push_to_sheets(sheet, df):
    '''This function takes in the sheet and the
    dataframe'''
    sheet.clear()
    set_with_dataframe(worksheet=sheet, dataframe=df, include_index=False,
                       include_column_header=True, resize=True)


if __name__ == '__main__':
    client = get_connect_sheet()
    sheet = client.open('test_sheet')
    print(sheet.worksheets())
