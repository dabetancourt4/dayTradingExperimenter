'''
Created on Jan 29, 2022

@author: david
'''

import requests
import csv
from matplotlib import pyplot as plt
from datetime import datetime
from time import sleep
import statistics

#dabetancourt4 API Key: YL3BRPOWW1UD12VA
#davidseamon12 API Key: OOW3ZHH028NNAMQN

#Inputs
input_ticker = 'SNAP'
input_time_interval = 1
input_pct_buy = 0.01
input_pct_sell = 0.01

def calculate_return(ticker, time_interval, pct_buy, pct_sell, year, month):
    
    #Read in the API data and store the times and close values in lists
    time_interval_string = str(time_interval) + 'min'
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=' + ticker + '&interval=' + time_interval_string + '&slice=year' + str(year) + 'month' + str(month) + '&apikey=OOW3ZHH028NNAMQN'
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        data_array = list(cr)
    
    data_close = []
    data_times = []
    for i in range(1,len(data_array)):  
        curr_dt = datetime.strptime(data_array[i][0], '%Y-%m-%d %H:%M:%S')
        if  (curr_dt.hour*60 + curr_dt.minute < 570) or (curr_dt.hour*60 + curr_dt.minute > 960):
            continue
        data_times.insert(0,curr_dt)
        data_close.insert(0,float(data_array[i][4]))
    
    #Translate the 1 X n lists of times and close values to m X n arrays where each m array is one day's worth of data
    times_by_day = []
    close_by_day = []

    i = 0
    j = 0
    while i < len(data_times):
        start_index = i
        end = False
        j = i
        
        while end == False:
            try:
                if (data_times[j].hour > data_times[j+1].hour):
                    end_index = j
                    i = end_index + 1
                    times_by_day.append(data_times[start_index:end_index+1])
                    close_by_day.append(data_close[start_index:end_index+1])
                    
                    end = True
                else:
                    j += 1
            except IndexError:
                end_index = j
                end = True
                i = len(data_times)
        
    
    
    #Go through the data day by day and execute the designated trades
    hit_pct_buy_times = []
    hit_pct_buy_close = []
    hit_pct_sell_times = []
    hit_pct_sell_close = []
    gain_loss = []
    count_hits = 0
    count_day_end = 0
    count_prof = 0
    
    #iterate through every day in the month
    for m in range(1, len(times_by_day)):
        n = 0
        start_val = close_by_day[m-1][-1]
        hit = False
        buy_type = ''
        buy_val = 0
        
        #iterate through each [time interval] in the day
        for n in range(0, len(times_by_day[m])):
            curr_val = close_by_day[m][n]
            
            # short sell a peak or buy a dip if the pct_buy is hit
            if ( hit == False and ((abs(curr_val - start_val)) / curr_val) > pct_buy):
                hit_pct_buy_times.append(times_by_day[m][n])
                hit_pct_buy_close.append(close_by_day[m][n])
                hit = True
                buy_val = close_by_day[m][n]
                if (buy_val > start_val): buy_type = 'peak'
                elif (buy_val < start_val): buy_type = 'dip'
            
            # sell after buying a dip if the pct_sell is hit
            elif ( hit == True and buy_type == 'dip' and ((curr_val - buy_val) / curr_val) > pct_sell ):
                hit_pct_sell_times.append(times_by_day[m][n])
                hit_pct_sell_close.append(close_by_day[m][n])
                gain_loss.append(buy_val*0.02)
                count_hits += 1
                count_prof += 1
                break
            
            # buy after short selling a peak if the pct_sell is hit
            elif ( hit == True and buy_type == 'peak' and -1*((curr_val - buy_val) / curr_val) > pct_sell ):
                hit_pct_sell_times.append(times_by_day[m][n])
                hit_pct_sell_close.append(close_by_day[m][n])
                gain_loss.append(buy_val*0.02)
                count_hits += 1
                count_prof += 1
                break
            
            # offload the position at the end of the day
            elif (hit == True and n == len(times_by_day[m]) - 1):
                hit_pct_sell_times.append(times_by_day[m][n])
                hit_pct_sell_close.append(close_by_day[m][n])
                if (buy_type == 'dip'): 
                    gain_loss.append(close_by_day[m][n] - buy_val)
                    if (close_by_day[m][n] > buy_val): count_prof += 1
                elif (buy_type == 'peak'): 
                    gain_loss.append(buy_val - close_by_day[m][n])
                    if (buy_val > close_by_day[m][n]): count_prof += 1
                count_day_end += 1
        
    #Calculate the net profit/loss for the month
    result = 0
    for i in range(len(gain_loss)):
        result += gain_loss[i]
        

    plt.plot(data_times,data_close, 'g-')
    plt.plot(hit_pct_buy_times, hit_pct_buy_close, 'yo')
    plt.plot(hit_pct_sell_times, hit_pct_sell_close, 'ro')
    plt.xticks(data_times, data_times)
    plt.show()
    #formatted_list = [ '%.2f' % elem for elem in gain_loss]
    #print(formatted_list)
    #print('Month:', month, 'Mean:', round(statistics.mean(gain_loss),2), 'Hit:', count_hits, "Day Ends:", count_day_end)
    #print('')
    

    return [round(result,2), count_hits, count_day_end, count_prof]
    
# print(calculate_return(input_ticker, input_time_interval, input_pct_buy, input_pct_sell, 1, 1))


return_arr = []
hit_arr = []
miss_arr = []
prof_arr = []
for year in range (1,2): 
    print('next year')
    for month in range(2,3):
        print(return_arr) 
        sleep(20)
        curr_val = calculate_return(input_ticker, input_time_interval, input_pct_buy, input_pct_sell, year, month)
        return_arr.append(curr_val[0])
        hit_arr.append(curr_val[1])
        miss_arr.append(curr_val[2])
        prof_arr.append(curr_val[3])
print('returns:', return_arr)
#print('hits:', hit_arr)
#print('misses:', miss_arr)
#print('profit count:', prof_arr)

print('monthly mean:', statistics.mean(return_arr))
print('monthly st dev:', statistics.pstdev(return_arr))
print('two year sum:', sum(return_arr))
print('hit pct:', (float(sum(hit_arr)) / float((sum(hit_arr) + sum(miss_arr)))))
print('profit pct:', float(sum(prof_arr)) / float((sum(hit_arr) + sum(miss_arr))))

