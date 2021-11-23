from utils import parse_date_2, parse_date_3


def get_1(self, url):
    #no changes needed
    if self['allChosen']:
        return url
    
    elems = self['actualValues']
    chosen = elems[self['chosen']]
    url.args['for-rent-by'] = chosen
    return url
    
    
def get_2(self, driver):
    #no changes needed
    if self['allChosen']:
        return

    elems = self['actualValues']
    chosen = [elems[i] for i in self['chosen']]
    for element in chosen:
        driver.execute_script(f'$(\'[for="form-unittype[]-&attributeMap[unittype_s]=[{element.lower()}]"]\').click()')
    
def get_3(self, url):
    if self['allChosen']:
        return url

    minimum = 0
    maximum = 5000
    start = self['start']
    end = self['end']

    if start <= minimum:
        start = ''
    if end >= maximum:
        end = ''

    price = f'{start}__{end}'
    url.args['price'] = price

    return url

def get_4(self, listing_value):
    if listing_value == 'N/A' or self['allChosen']:
        return True

    date_value = parse_date_2(listing_value)
    return self['start'] <= date_value <= self['end']

def get_5(self, listing_value):
    if listing_value == 'N/A' or self['allChosen']:
        return True

    date_value = parse_date_3(listing_value)
    return self['start'] <= date_value <= self['end']


def set_1(self, filter_dict):
    if 'chosen' in filter_dict:
        self['chosen'] = self['displayValues'].index(filter_dict['chosen'])
    self['allChosen'] = filter_dict['allChosen']


def set_2(self, filter_dict):
    if 'chosen' in filter_dict:
        self['chosen'] = [self['displayValues'].index(i) for i in filter_dict['chosen']]
    self['allChosen'] = filter_dict['allChosen']

def set_3(self, filter_dict):
    if 'start' in filter_dict:
        self['start'] = filter_dict['start']

    if 'end' in filter_dict:
        self['end'] = filter_dict['end']

    self['allChosen'] = filter_dict['allChosen']


set_5 = set_4 = set_3

def set_6(self, filter_dict):
    if 'chosen' in filter_dict:
        self['chosenCities'] = filter_dict['chosen']
    self['allChosen'] = filter_dict['allChosen']
