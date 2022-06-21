'''
Created on May 28, 2022

@author: david
'''

import tkinter as tkfrom root import trading_strategy as ts
from time import sleep
import statistics
from PIL import ImageTk, Image 

#API Key: OOW3ZHH028NNAMQN

gui = tk.Tk()

def run_scenario(api_key, ticker, pct_buy, pct_sell, stop_loss, max_month):
    return_arr = []
    mean_arr = []
    
    #Iterate through each month that the user wants to investigate
    for month in range(1,max_month+1):
        #For debugging
        print(return_arr) 
        #Delay required due to free API limits on calls per minute
        sleep(5)
        #Gets the raw ticker data from the API 
        times_by_day, close_by_day, time_data, close_data = ts.get_ticker_data(api_key, ticker, month)
        #Calculates the return using the given strategy for the current month
        curr_val = ts.calculate_return(float(pct_buy)/100, float(pct_sell)/100, float(stop_loss)*-1/100, times_by_day, close_by_day, time_data, close_data, month, max_month)
        return_arr.append(curr_val[0])
        mean_arr.append(statistics.mean(close_data))
    #For debugging
    print('returns:', return_arr)
    
    #Summary statistics 
    monthly_mean = statistics.mean(return_arr)
    print('monthly mean:', monthly_mean)
    print('monthly median:', statistics.median(return_arr))
    print('monthly st dev:', statistics.pstdev(return_arr))
    print('two year sum:', sum(return_arr))
    
    bg_color = 'white'
    if monthly_mean > 0: bg_color = 'light green'
    elif monthly_mean < 0: bg_color = 'red'
    
    result_mean_label = tk.Label(text='Average Monthly Return: ' + str(round(monthly_mean*100/statistics.mean(mean_arr), 2)) + '%', bg=bg_color)
    result_mean_label.grid(row=9, column=1, sticky='N')
    result_sd_label = tk.Label(text='Monthly Standard Deviation: ' + str(round(statistics.pstdev(return_arr)*100/statistics.mean(mean_arr), 2)) + '%', bg='white')
    result_sd_label.grid(row=9, column=2, sticky='N')
    
    
if __name__ == "__main__":
    gui.title('Day Trading Simulator')
    gui.configure(bg='white')
    
    explanation_title = tk.Label(text='Description:', bg='white', font='bold 12')
    explanation_1 = tk.Message(text='This simulator is based on the hypothesis that once a stock price changes by a certain amount in a day, it is more likely to reverse direction (move toward 0%) than continue moving in the same direction for the remainder of the day.', width=500, bg='white')
    explanation_2 = tk.Message(text='The algorithm starts by noting the final price of the stock when the market closed the previous day. It them iterates through the next day\'s prices, and opens a position when the daily % change reaches a certain level. It closes the position when a % profit is made, a % loss is incurred, or the trading day ends.', width = 500, bg='white')
    example_title = tk.Label(text='Example:', bg='white', font='bold 12')
    explanation_3 = tk.Message(text='A) Previous day\'s close price\nB) Daily % price change to trigger a position to open\nC) % gain to trigger the position to close (take profit)', width=500, bg='white')
    diagram_image = ImageTk.PhotoImage(Image.open("./example_diagram.jpg").resize((500, 250), Image.ANTIALIAS))
    diagram = tk.Label(image=diagram_image, bg='white')
    
    input_title = tk.Label(text='Inputs:', bg='white', font='bold 12')
    ticker_label = tk.Label(text="Stock ticker:", bg='white')
    ticker_input = tk.Entry(width=10)
    ticker_input.insert(0,'SNAP')
    pct_buy_label = tk.Label(text= "% Change to trigger a position to open:", bg='white')
    pct_buy_input = tk.Entry(width=6)
    pct_buy_pct = tk.Label(text='%', bg='white')
    pct_buy_input.insert(0,'2')
    pct_sell_label = tk.Label(text="% Gain to close position (take profit):", bg='white')
    pct_sell_input = tk.Entry(width=6)
    pct_sell_pct = tk.Label(text='%', bg='white')
    pct_sell_input.insert(0,'2')
    stop_loss_label = tk.Label(text="% Loss to close position (stop loss):", bg='white')
    stop_loss_input = tk.Entry(width=6)
    stop_loss_pct = tk.Label(text='%', bg='white')
    stop_loss_negative = tk.Label(text='-', bg='white')
    stop_loss_input.insert(0,'5')
    month_label = tk.Label(text="# Previous months to simulate:", bg='white')
    month_input = tk.Scale(orient='horizontal', length=180, from_=1, to=12, bg='white')
    enter_button = tk.Button(text = 'Run Scenario', command = lambda: run_scenario('OOW3ZHH028NNAMQN', ticker_input.get().upper(), pct_buy_input.get(), pct_sell_input.get(), stop_loss_input.get(), int(month_input.get())))
    results_title = tk.Label(text='Results:', bg='white', font='bold 12')
    
    explanation_title.grid(row=1,column=0, padx=25, sticky='SW', pady=5)
    explanation_1.grid(row=2,column=0, padx=20, rowspan=2, sticky='NW')
    explanation_2.grid(row=4, column=0, padx=20, rowspan=2, sticky='NW')
    example_title.grid(row=6, column=0, padx=25, rowspan=1, sticky='SW')
    explanation_3.grid(row = 7, column=0, padx=20, rowspan=2, sticky='NW')
    diagram.grid(row=9,column=0,padx=20, sticky='NW')
    
    input_title.grid(row=1, column=1, padx=25, pady=5, sticky='W')
    ticker_label.grid(row=2, column=1, padx=25, pady=5, sticky='E')
    ticker_input.grid(row=2, column=3, sticky='W')
    pct_buy_label.grid(row=3, column=1, padx=25, pady=5, sticky='E')
    pct_buy_input.grid(row=3, column=3, sticky='W')
    pct_buy_pct.grid(row=3, column=3)
    pct_sell_label.grid(row=4, column=1, padx=25, pady=5, sticky='E')
    pct_sell_input.grid(row=4, column=3, sticky='W')
    pct_sell_pct.grid(row=4, column=3)
    stop_loss_label.grid(row=5, column=1, padx=25, pady=5, sticky='E')
    stop_loss_negative.grid(row=5,column=2, sticky='W')
    stop_loss_input.grid(row=5, column=3, sticky='W')
    stop_loss_pct.grid(row=5, column=3)
    month_label.grid(row=6, column=1, padx=25, pady=5, sticky='E')
    month_input.grid(row=6, column=3, columnspan=2, sticky='W')
    enter_button.grid(row=7, column=1, padx=35, pady=5, sticky='W')
    results_title.grid(row=8, column=1, padx=25, sticky='SW', pady=20)
    
    gui.mainloop()

