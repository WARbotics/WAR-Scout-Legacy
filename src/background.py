from time import sleep
import dataCollection as data
import main

last_len = None
holder = None
while True:
    
    holder = len(data.getSheet('B2:R'))
    if holder != last_len:
        last_len = holder
        main.Team().find_data()
    sleep(120)
    print()