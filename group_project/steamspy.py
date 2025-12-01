import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import csv
import requests

from bs4 import BeautifulSoup


response = requests.get(url="https://steamspy.com/#tab-trending")
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')    
game_data = soup.find_all('td', class_='treleasedate')


with open('steamspy.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(game_data)



print('data written to steamspy.json')
