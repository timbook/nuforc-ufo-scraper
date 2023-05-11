import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

nuforc_base = 'https://nuforc.org/webreports/'

print("Getting initial NUFORC web data...")
res = requests.get(nuforc_base + 'ndxevent.html')
soup = BeautifulSoup(res.text, 'lxml')

a_tags = soup.find('table').find_all('a')
date_links = [a.attrs['href'] for a in a_tags]
def link_to_df(link):
    date_url = nuforc_base + link
    df = pd.read_html(nuforc_base + date_links[0])[0]
    return df

print("Pulling individual chunks of data by month,")
print("this will take several minutes...")
dfs = [link_to_df(link) for link in date_links]
df = pd.concat(dfs)

colname_map = {
    'Date / Time': 'datetime',
    'City': 'city',
    'State': 'state',
    'Country': 'country',
    'Shape': 'shape',
    'Colors Reported': 'colors'
}

df.rename(columns=colname_map, inplace=True)
df = df[['datetime', 'city', 'state', 'country', 'shape']]

print("Scrape complete! Saving now...")
df.to_csv('ufo.csv', index=False)
