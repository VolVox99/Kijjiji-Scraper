from fields import fields
from bs4 import BeautifulSoup
from utils import *
from headers import Headers


headers = Headers()

cont = 'cont'
def scrape_listing(url, sesh, options):
    fields_dict = {}

    headers.update('referer', url)
    
    html = get_req(sesh, url, headers.headers)
    soup = BeautifulSoup(html, 'html.parser')

    if is_blocked(soup):
        #return empty dict
        return fields_dict

    for field in fields:
        value = field['get'](soup)
        fields_dict[field['name']] = value
        if not options.option_matches(field, value):
            return cont

    fields_dict['URL'] = url

    return fields_dict



