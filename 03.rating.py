import os
import time
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup

def main():
    start_time = time.time()
    print('Saving the output of extracted information')
    csv_file = 'testiskontol.csv'
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

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser') 

    viewe = []
    likes_list = []

    fav = soup.find('ul' , class_ = 'grade_area').find_all_next('em', class_='cnt')
    for likes in fav:
            info = likes.get_text()
            likes_list.append(info)

    likes_combined = '|'.join(likes_list)
    viewe.append(likes_combined)
    return viewe

def save_product(viewe):
    data =   {'view|sub|rate' : viewe}
    df= pd.DataFrame(data, index=[0])
    df.to_csv('rating.csv', sep='|', index=False, mode='a+', header=False)

main()
