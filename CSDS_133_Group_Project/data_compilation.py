from types import NoneType
import numpy as np
import pandas as pd

import csv


data = {
    'Jan' : [],
    'Feb' : [],
    'Mar' : [],
    'Apr' : [],
    'May' : [],
    'Jun' : [],
    'Jul' : [],
    'Aug' : [],
    'Sep' : [],
    'Oct' : [],
    'Nov' : [],
    'Dec' : [],
}

f2p = {
    'Jan' : [],
    'Feb' : [],
    'Mar' : [],
    'Apr' : [],
    'May' : [],
    'Jun' : [],
    'Jul' : [],
    'Aug' : [],
    'Sep' : [],
    'Oct' : [],
    'Nov' : [],
    'Dec' : [],
}

#NOTE: no checks for overlap rn, high chance of duplicates
def dump_csv(filepath, date_index, price_index, player_count_index=-1, review_count_index=-1):
    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        n = 0
        
        for row in csv_reader:
            # Skip header row
            if n == 0:
                n += 1
                continue
            # Skip if price not reported
            if row[price_index] == 'N/A':
                continue

            # Insert to table by month
            month = row[date_index]
            if month[0:3] not in data.keys():
                match month[5:7]:
                    case '01':
                        month = 'Jan'
                    case '02':
                        month = 'Feb'
                    case '03':
                        month = 'Mar'
                    case '04':
                        month = 'Apr'
                    case '05':
                        month = 'May'
                    case '06':
                        month = 'Jun'
                    case '07':
                        month = 'Jul'
                    case '08':
                        month = 'Aug'
                    case '09':
                        month = 'Sep'
                    case '10':
                        month = 'Oct'
                    case '11':
                        month = 'Nov'
                    case '12':
                        month = 'Dec'

            # Add a tuple of (player count, price) to the data table
            players = ""
            if player_count_index != -1:
                players = row[player_count_index]
                try:
                    players = int(players)
                except:
                    p = players.replace(',', "").split("\xa0..\xa0")
                    players = (int(p[0]) + int(p[1])) / 2
            else:
                players = row[review_count_index]

                if players == '':
                    continue

                # About 1 in 70 people review a game on average
                players = int(players) * 70


            price = row[price_index]
            if price[0:1] == '$':
                price = price[1:]
            if price == 'Free':
                price = 0.0
                            
            if month == '':
                continue

            t = (players, price)
            if price == 0.0:
                f2p[month[0:3]].append(t)
            else:
                data[month[0:3]].append(t)



# Steamspy
dump_csv('./data/SteamSpy.csv', 2, 3, player_count_index=5)
# Gamalyics
dump_csv('./data/GamalyicsFiltered.csv', 1, 3, player_count_index=2)
# Webscraped
dump_csv('./data/WebScrapeFiltered.csv', 3, 4, review_count_index=1)

 
# Sort the table rows
sorted_keys = sorted(data.keys(), key=lambda k: len(data[k]), reverse=True)

priced = pd.DataFrame()
free = pd.DataFrame()

for key in sorted_keys:
    priced[key] = pd.Series(data[key])

sorted_keys = sorted(f2p.keys(), key=lambda k: len(f2p[k]), reverse=True)

for key in sorted_keys:
    free[key] = pd.Series(f2p[key])

print(priced)
print(free)



# NOTE: Usage of data from the frame will almost certainly need to be in a for loop format due to the use of tuples
# NOTE: Most of the rows end with an arbitrary number of NaNs, these will need to be accounted for



