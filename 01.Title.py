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
judul = []
pengarang = []
favorit = []


req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, 'html.parser') 

#class marker at html page
genres = soup.find('div', class_='card_wrap genre')
info = genres.find_all('div', class_='info')

#extract data
for title in info:
    name = title.find('p', class_='subj').get_text()
    author = title.find('p', class_='author').get_text()
    like = title.find('em', class_='grade_num').get_text().replace('JT', '00000').replace('.', '').replace(',','')
   
    #collect data on list
    judul.append(name)
    pengarang.append(author)
    favorit.append(like)

#collect list into one 
data = {'Judul': judul,'Pengarang': pengarang, 'Favorit': favorit}

#counting records
print(f'Num of obtained records: {len(judul)}')

df = pd.DataFrame(data)

df.to_csv('webtoontitle.csv', sep='|',index=False)