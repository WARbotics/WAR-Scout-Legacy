import time
import dataCollection as data
import main

last_len = None
while True:
    time.sleep(120)
    if len(data.getSheet('B2:P')) != last_len:
        last_len = len(data.getSheet('B2:P'))
        main.Team().find_data()
        print()