import os
import time
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup

#load url to webtoon title
def main():
    start_time = time.time()
    #saving file
    print('Saving the output of extracted information')
    csv_file = 'sinopsis.csv'

    #accesing url to webtoon title
    if os.path.exists(csv_file):
        os.remove(csv_file)
    with open('url.csv') as file:
        csv_reader = csv.DictReader(file)
        for csv_row in csv_reader:
            scraped_data = scrape(csv_row['url'])
            save_product(*scraped_data)

    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f seconds' % time_difference)

def scrape(url):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}
    #class marker at html page
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser') 
    genres = soup.find_all('div', class_='aside detail')
    
    #container
    sinopsis = []

    for title in genres:
        summary = title.find('p', class_='summary').get_text()
        sinopsis.append(summary)
    return sinopsis

def save_product(sinopsis):
    data = ({'Sinopsis' : sinopsis})
    df= pd.DataFrame(data, index=[0])
    df.to_csv('sinopsis.csv', index=False, mode='a+', header=True)

main()
