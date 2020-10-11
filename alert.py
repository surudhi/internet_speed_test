import speedtest as st
import pandas as pd
import win32api

def main():
    speed=pd.read_csv('int_speed.csv')
    avrg=float("{:.3f}".format(speed['Download'].mean()))
    print('Average Speed: ',avrg,'Mb/s')
    speed_test = st.Speedtest()
    speed_test.get_best_server()
    download = speed_test.download()
    download = round(download / (10**6), 3)
    print('Current Download Speed: ',download,'Mb/s')
    if(avrg>download):
        win32api.MessageBox(0, 'Internet bandwidth is less than expected limit!', 'Speed Alert')

if __name__ == "__main__":
    main()
