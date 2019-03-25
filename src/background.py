from time import sleep
import dataCollection as data
import main

last_len = None
holder = None
while True:
    try:
        holder = len(data.getSheet('B2:R'))
        if holder != last_len:
            last_len = holder
            main.Team().find_data()
        sleep(180)
    except:
        last_len = None
        holder = None
        print('Failed')
        sleep(300)
    print()