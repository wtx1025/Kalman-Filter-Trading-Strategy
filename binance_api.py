import time
import requests
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as py 

print(int(time.time()))

base_url='https://fapi.binance.com'

kline_url='/fapi/v1/klines'

#時間戳改成時間字串格式
def shift_time(time_stamp):
    struct_time=time.localtime(time_stamp)
    timestring=time.strftime("%Y-%m-%d %H:%M:%S",struct_time)

    return timestring

#時間字串格式改成時間戳
def convert_time(time_string):
    struct_time=time.strptime(time_string,"%Y-%m-%d %H:%M:%S") #轉成時間元組
    time_stamp=int(time.mktime(struct_time)) #轉成時間戳
    
    return time_stamp

#抓取歷史價格資料
def fetch(symbol,interval,limit,start_Time,end_Time):

    start_Time=convert_time(start_Time)*1000
    end_Time=convert_time(end_Time)*1000

    url=base_url + kline_url +'?' + 'symbol=' + symbol + '&interval=' + interval + '&limit=' + limit + '&startTime=' + str(start_Time) + '&endTime=' + str(end_Time)
    print(url)

    resp=requests.get(url)
    data=resp.json()
    df=pd.DataFrame(data)[[0,1,2,3,4,5]]

    df.columns=['Time','Open','High','Low','Close','Volume']
    end=df['Time'].index[df.shape[0]-1]
    
    df['Time']=df['Time']/1000
    df['Time']=df['Time'].apply(shift_time)
    df.set_index('Time',inplace=True)
    print(df)
    
    return df

def save(symbol,interval,limit,start_Time,end_Time):

    df=fetch(symbol,interval,limit,start_Time,end_Time)
    while(convert_time(df.index[df.shape[0]-1]) < convert_time(end_Time)):
        # df=df.append(fetch(symbol,interval,limit,shift_time(convert_time(df.index[df.shape[0]-1])+14400),end_Time))
        df = pd.concat([df, fetch(symbol, interval, limit, shift_time(convert_time(df.index[df.shape[0]-1]) + 14400), end_Time)])
    
    df.to_csv("C:\\Users\\王亭烜\\Desktop\\School\\碩二上\\Applied Bayes Method\\Final Project\\Data\\btc4h.csv")

save('BTCUSDT','4h','1000','2022-01-01 00:00:00','2024-11-30 00:00:00')
print('[***************Fetch data 100% done***************]')