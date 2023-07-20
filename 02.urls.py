import pandas as pd
import requests
from bs4 import BeautifulSoup

#refference url
url = 'https://www.webtoons.com/id/genre#'

#headers
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

#data collected will be stored on the list
alamat_url = []

req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, 'html.parser') 

#class marker at html page
genres = soup.find('div', class_='card_wrap genre')
loh = genres.find_all('a')

#extract data
for urls in loh:
    alamat = urls.get('href')
    
    #collect data on list
    alamat_url.append(alamat)

print(f'Num of obtained records: {len(alamat_url)}')

#input number to display few first data 
show = input('Type a number to show list:')
x = int(show)
i = 0
while True:
    print(alamat_url[i])
    i += 1
    if i == x:
        break

data_url = {'url' : alamat_url}
df = pd.DataFrame(data_url)

#number of data deleted
num = input('Type number to delete first few data:')
N = int(num)
#deleting the first data
df = df.iloc[N:,:]
print(f'Deleting {N} data...')

df.to_csv('url.csv', sep='|',index=False)
