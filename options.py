from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from furl import furl
from url import DEFAULT_URL
from json import loads
from option_getters_setters import *
from utils import parse_date_1


class Options:
    def __init__(self, app = None):
        try:
            with open('filters.json') as f:
                filters_dict = loads(f.read())
        except:
            if app: app.stop()
            raise ValueError('ERROR: Filters not written by GUI, restart')


        self.filter_option = {
                'displayValues': ['Apartment', 'Condo', 'Basement', 'House', 'Townhouse', 'Duplex/Triplex'],
                'actualValues': ['apartment', 'condo', 'basement-apartment', 'house', 'townhouse', 'duplex-triplex'],
                # 'chosen': [1, 3],
                # 'allChosen': False,
                'get': get_2,
                'set': set_2,
                'name': 'Unit Type'
        }

        self.url_options = [
            {
                # 'start': 0,
                # 'end': 5000,
                # 'allChosen': False,
                'get': get_3,
                'set': set_3,
                'name': 'Price Range'
            }, 
            {
                'displayValues': ['Owner', 'Professional'],
                'actualValues': ['ownr', 'reprofessional'],
                # 'chosen': 0,
                # 'allChosen': False,
                'get': get_1,
                'set': set_1,
                'name': 'For Rent By'
            },
        ]

        self.cities = {
            # 'chosenCities': [],
            # 'allChosen': True,
            'name': 'Cities',
            'set': set_6,
        }

        self.date_options = [
            {   
                'field': 'Move-In Date',
                # 'allChosen': False,
                'get': get_4,
                'set': set_4,
                'name': 'Move-In Date'
            },
            
            {   
                'field': 'Date Posted',
                # 'start': '',
                # 'end': '',
                # 'allChosen': False,
                'get': get_5,
                'set': set_5,
                'name': 'Date Posted'
            },
        ]

        options = [self.filter_option] + self.url_options + [self.cities] + self.date_options

        try:
            self.continue_file = filters_dict['Options'].get('continueFile', False)
        
            #load options from file that was configured by GUI
            for option in options:
                option['set'](option, filters_dict[option['name']])

            for val in self.date_options:
                if 'start' in val:
                    val['start'] = parse_date_1(val['start'])

                if 'end' in val:
                    val['end'] = parse_date_1(val['end'])

        except:
            if app: app.stop()
            raise ValueError('ERROR: Invalid filter values, restart GUI')
        
        self.date_option_fields = [option['field'] for option in self.date_options]

            
    def get_location_urls(self, driver):
        if self.cities.get('allChosen'):
            return [DEFAULT_URL]

        locations = []

        driver.get(DEFAULT_URL)

        for city in self.cities['chosenCities']:
            driver.find_element_by_css_selector('#SearchLocationPicker').click()
            inp = driver.find_element_by_css_selector('#SearchLocationSelector-input')
            inp.clear()
            action = ActionChains(driver)
            action.click(on_element = inp)
            action.send_keys_to_element(inp, city)
            action.pause(1.5)
            action.send_keys_to_element(inp, Keys.RETURN)
            action.perform()
            sleep(3)
            driver.find_element_by_css_selector('button[role=checkbox]').click()
            sleep(2)
            driver.find_element_by_css_selector('div.bottomBarWrapper-1909455774.bottomBarWrapper__expanded-497052036 > div > div:nth-child(3) > button').click()
            locations.append(driver.current_url)

        return locations


    def get_option_url(self, driver, url):
        driver.get(url)

        #open filters page
        driver.find_element_by_css_selector('button.addFiltersButton-2536109863.button-1997310527.button__medium-1066667140').click()

        self.filter_option['get'](self.filter_option, driver)
        
        #apply filters
        driver.find_element_by_css_selector('button.resultsButton-1350999047.button-1997310527.button__primary-1681489609.button__medium-1066667140').click()

        new_url = furl(driver.current_url)
        new_url.args['ad'] = ''
        del new_url.args['ad']

        for option in self.url_options:
            new_url = option['get'](option, new_url)
        
        return str(new_url)


    def option_matches(self, field, listing_value):
        name = field['name']
        try:
            idx = self.date_option_fields.index(name)
        except ValueError:
            return True

        option = self.date_options[idx]
        return option['get'](option, listing_value)