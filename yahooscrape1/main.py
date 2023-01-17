import os

try:
    import send_mail
    from main import capture_data
    from sheet_connect import get_connect_sheet
    from sheet_connect import push_to_sheets
    import pandas as pd
    import os
except Exception as e:
    send_mail.send_email(e)
    os._exit(0)

#This scrapes the data from Yahoo Finance
try:
    data = capture_data()
except Exception as e:
    send_mail.send_email(e)
    os._exit(0)

try:
    #This imports the service account credentials that will allow us access the sheet
    client = get_connect_sheet()
    #Once the connection has been made, the Google Sheet can now be accessed
    push_sheet = client.open('test_sheet')
    #opening the data sheet
    data_push = push_sheet.worksheet('data2')
    data_push_df = pd.DataFrame.from_dict(data_push.get_all_records())

except Exception as e:
    send_mail.send_email(e)
    os._exit(0)


def append_new_data(df, sheet_name):
    """This function takes in the dataframe and the name of the sheet you wish
    to append the data to """

    values = df.values.tolist()
    push_sheet.values_append(sheet_name, {'valueInputOption': 'USER_ENTERED'},
                             {'values': values})

print(data)

try:
    if len(data_push_df) == 0:
        push_to_sheets(data_push, data)
    else:
        append_new_data(data,'data2')
except Exception as e:
    print('Could not append')
    send_email(e)
    os._exit(0)


