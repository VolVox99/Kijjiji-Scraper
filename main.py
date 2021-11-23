import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
from scrape_listing import scrape_listing
from fields import field_names
from url import BASE_URL
from random import random
from headers import Headers
from utils import *
from options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from os import environ


#TODO: fix
environ['WDM_LOG_LEVEL'] = '0'


def pause():
    sleep(random() * 10 + 5)


def second_main(options, app = None,):
    outFile = 'output.csv'

    continue_file =  options.continue_file

    with open(outFile, 'r+' if continue_file else 'w', newline = '', encoding = 'utf-8') as csvfile:
        past_listings = set()
        if continue_file:
            csv_reader = csv.DictReader(csvfile) 
            past_listings.update([row['URL'] for row in csv_reader])
            print('continuing from', outFile)
        
        csv_writer = csv.DictWriter(csvfile, fieldnames = field_names)
        if not continue_file:
            csv_writer.writeheader()

        row_num = 0
        headers = Headers()

        with requests.Session() as sesh:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            with webdriver.Chrome(executable_path =  ChromeDriverManager(log_level = 0).install(), options = chrome_options) as driver:
                locations = [options.get_option_url(driver, location) for location in options.get_location_urls(driver)]

            for url in locations:
                print('starting on:', url)
                    
                running = True
                location_listings = set()

                #loop until the end of pages
                while running:

                    soup = BeautifulSoup(get_req(sesh, url, headers.headers), 'html.parser')

                    while is_blocked(soup):
                        pause()
                        soup = BeautifulSoup(get_req(sesh, url, headers.headers), 'html.parser')
                        print('sleeping')

                    next_page_link = soup.find(title = 'Next')

                    #get url of all listings, concatenate root domain
                    listings = [BASE_URL + i.get('href') for i in soup.select('div.info > div > div.title > a')]
                    location_listings.update(listings)
            
                    if next_page_link is None:
                        running = False
                        break

                    url = BASE_URL + next_page_link.get('href')

                #remove listings that were in past_listings (the file)
                location_listings = location_listings.difference(past_listings)
                print('new listings (non duplicates) found:' if continue_file else 'listings found:', len(location_listings))
                #after accumulating all listings for the location, process them
                for listing in list(location_listings):

                    #pass in url and parse data from listing
                    #check for blocked from making requests, sleep for cooldown in case
                    while not (row_dict := scrape_listing(listing, sesh, options)):
                        pause()
                        print('sleeping')
                    
                    #options didn't match
                    if row_dict == 'cont':
                        continue

                    csv_writer.writerow(row_dict)
                    row_num += 1
                    print(row_num)

            print('\n\nFINISHED')
            if app: app.stop()

def main(app):
    options = Options(app)
    try:
        second_main(options, app)
    except Exception as e:
        print(f'ERROR: {e}')
    

if __name__ == '__main__': 
    main()