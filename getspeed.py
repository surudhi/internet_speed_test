import speedtest as st

#Obtain results from speedtest
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
