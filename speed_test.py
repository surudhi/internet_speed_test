
import speedtest as st
import pandas as pd
from datetime import datetime
import schedule
import time
import sys
import csv

def get_new_speeds():
    speed_test = st.Speedtest()
    speed_test.get_best_server()

    # Get ping (miliseconds)
    ping = speed_test.results.ping
    # Perform download and upload speed tests (bits per second)
    download = speed_test.download()
    upload = speed_test.upload()

    # Convert download and upload speeds to megabits per second
    download_mbs = round(download / (10**6), 2)
    upload_mbs = round(upload / (10**6), 2)
    ping=float("{:.2f}".format(ping))
    return (ping, download_mbs, upload_mbs)

def update_csv(internet_speeds):
    # Get today's date in the form Month Day, Year Hour:Min:Sec
    date_today = datetime.today().strftime("%B %d, %Y %H:%M:%S")
    # File with the dataset
    csv_file_name = "int_speed.csv"

    # Load the CSV to update
    try:
        csv_dataset = pd.read_csv(csv_file_name, index_col="Date")
    # If there's an error, assume the file does not exist and create\
    # the dataset from scratch
    except:
        csv_dataset = pd.DataFrame(
            list(),
            columns=["Ping", "Download", "Upload"]
        )

    # Create a one-row DataFrame for the new test results
    results_df = pd.DataFrame(
        [[ internet_speeds[0], internet_speeds[1], internet_speeds[2] ]],
        columns=["Ping", "Download", "Upload"],
        index=[date_today]
    )

    updated_df = csv_dataset.append(results_df, sort=False)

    updated_df\
        .loc[~updated_df.index.duplicated(keep="last")]\
        .to_csv(csv_file_name, index_label="Date")

def end_sched():
    schedule.clear()
    speed=pd.read_csv('int_speed.csv')
    maxi=speed['Date'][speed.Download==speed.Download.max()]
    print(pd.to_datetime(maxi).dt.time)
    sys.exit()

def code():
    new_speeds = get_new_speeds()
    update_csv(new_speeds)

schedule.every(30).minutes.do(code)
schedule.every().day.do(end_sched)
while True:   
    # Checks whether a scheduled task  
    # is pending to run or not 
    schedule.run_pending() 
    time.sleep(1)
