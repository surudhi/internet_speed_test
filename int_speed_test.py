
from matplotlib import dates, rcParams
import matplotlib.pyplot as plt
import speedtest as st
import datetime as dt
import pandas as pd
import win32api
import schedule
import time
import sys
import csv

def get_new_speeds():
    servers=[]
    threads=None
    speed_test = st.Speedtest()
    speed_test.get_servers(servers)
    speed_test.download(threads=threads)
    speed_test.upload(threads=threads)
    speed_test.results.share()
    result=speed_test.results.dict()

    # Convert download and upload speeds to megabits per second
    download = speed_test.download()
    upload = speed_test.upload()
    result['download'] = round(download/ (10**6), 2)
    result['upload'] = round(upload / (10**6), 2)
    return result

def update_csv(internet_speeds):
    # Get today's date in the form Month Day, Year Hour:Min:Sec
    date_today = dt.datetime.today().strftime("%B %d, %Y %H:%M:%S")
    # File with the dataset
    csv_file_name = "int_speed.csv"
    # Load the CSV to update
    try:
        csv_dataset = pd.read_csv(csv_file_name, index_col="Date")
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

def create_plot(plot_file_name):
  speeds = pd.read_csv('int_speed.csv')
  speeds=speeds[-48:]  
  speeds['Date']=pd.to_datetime(speeds['Date'],errors='coerce')
  speeds['Time']=speeds['Date'].dt.strftime("%H:%M")
  rcParams['xtick.labelsize'] = 'xx-small'
  plt.plot(speeds['Time'],speeds['Download'], label='Download')
  plt.plot(speeds['Time'],speeds['Upload'],label='Upload')
  plt.title('Speed Test Results (24 hours)')
  plt.ylabel('Bandwidth in Mbps')
  plt.yticks(range(0,51,5))
  plt.ylim(0.0,50.0)
  plt.xlabel('Date/Time')
  plt.xticks(rotation='45')
  plt.savefig('speed test.png')
  plt.legend()
  plt.show()

def optimum_hour():
    result = get_new_speeds()
    new_speeds=[result['ping'],result['download'],result['upload']]
    update_csv(new_speeds)

def print_results():
    result=get_new_speeds()

    #Seperate client and server details
    server=result['server']
    client=result['client']
    result.pop('server')
    result.pop('client')

    #Print results
    print('\nSpeed Test Results\n')
    print("\n".join("{}\t{}".format(k, v) for k, v in result.items()))
    print('\nServer Details\n')
    print("\n".join("{}\t{}".format(k, v) for k, v in server.items()))
    print('\nClient Details\n')
    print("\n".join("{}\t{}".format(k, v) for k, v in client.items()))

def alert():
    speed=pd.read_csv('int_speed.csv')
    avrg=float("{:.3f}".format(speed['Download'].mean()))
    print('\nAverage/Expected Download Speed: ',avrg,'Mb/s')
    result=get_new_speeds()
    print('Current Download Speed: ',result['download'],'Mb/s')
    if(avrg>result['download']):
        win32api.MessageBox(0, 'Internet bandwidth is less than expected limit!', 'Speed Alert')

def end_sched():
    schedule.clear()
    speed=pd.read_csv('int_speed.csv')
    #Find optimum hour with maximum download speed
    speed['Hour']=pd.to_datetime(speed['Date']).dt.hour
    avg_spd=[]
    #Compute average for all hours
    for i in range(0,24):
        index=speed[speed['Hour']==i].index.tolist()
        avr_speed=speed['Download'].iloc[index].mean(axis=0)
        avg_spd.append(avr_speed)
    #Find the hour with max speed
    opt=avg_spd.index(max(avg_spd))
    opt=dt.time(opt,0,0)
    opt1=dt.time(opt.hour+1)
    print('\nOptimum time to browse:', opt, ' to', opt1)
    #Plot download speed data over last 24 hours
    plot_file_name = 'bandwidth.png'
    create_plot(plot_file_name)
    sys.exit()
    
def main():
    print_results()
    schedule.every(30).seconds.do(optimum_hour)
    schedule.every(30).seconds.do(alert)
    schedule.every(30).seconds.do(end_sched)
    while True:    
        schedule.run_pending() 
        time.sleep(1)
    
if __name__ == "__main__":
    main()
