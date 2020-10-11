import matplotlib.pyplot as plt
from matplotlib import dates, rcParams
import pandas as pd
import sys

def main():
  plot_file_name = 'bandwidth.png'
  create_plot(plot_file_name)
  sys.exit()

def create_plot(plot_file_name):
  df = read_data()
  make_plot_file(df, plot_file_name)

def read_data():
  df = pd.read_csv('int_speed.csv')
  return df[-24:]   # return data for last 48 periods (i.e., 24 hours)

def make_plot_file(last_24, file_plot_name):
  rcParams['xtick.labelsize'] = 'xx-small'
  plt.plot(last_24['Date'],last_24['Download'], 'b-')
  plt.title('Speed Test Results (24 hours)')
  plt.ylabel('Bandwidth in MBps')
  plt.xlabel('Date/Time')
  plt.xticks(rotation='45')
  plt.show()

if __name__ == '__main__':
  main()
