from time import sleep
import dataCollection as data
import main

last_len = None
while True:
    if len(data.getSheet('B2:R')) != last_len:
        last_len = len(data.getSheet('B2:R'))
        main.Team().find_data()
        print()
    sleep(120)