from url import BASE_URL


DEBUG = False
ERROR_VAL = "N/A"

def error_decorator(func, err = ERROR_VAL):
    def new_func(*args, **kwargs):
        try:
            return func(*args, **kwargs) or err
        except Exception as e:
            if DEBUG: print(e)
            return err
    
    return new_func

def concat_base_url(func):
    def new_func(*args, **kwargs):
        return BASE_URL + func(*args, **kwargs)
    return new_func


additional_field_names = ['Wi-Fi and More', 'Parking Included', 'Agreement Type', 'Move-In Date', 'Pet Friendly', 'Size (sqft)', 'Furnished', 'Appliances', 'Air Conditioning', 'Personal Outdoor Space', 'Smoking Permitted', 'Amenities', 'Elevator Accessibility Features', 'Barrier-free Entrances and Ramps', 'Visual Aids', 'Accessible Washrooms in Suite']



#grabs all values in card list, finds the one which matches the current field name, and returns the rest of it
def additional_field_get(soup, field_name):

    vals = [i.get_text('\n') for i in soup.select('.attributeCard-1535740193  li') if not 'groupItem-4214219251' in i.get('class')]

    current_val = ""
    for val in vals:
        if field_name in val:
            current_val = val
            break
    
    if not current_val:
        return ERROR_VAL

    return current_val.replace(field_name, '').strip()


def map_yes_no(soup):
    return {False: "No", True: "Yes"}[bool(soup)]

#, Richmond V6X1W7 BC, Canada -> 
#https://www.google.com/maps/search/,+Richmond+V6X1W7+BC,+Canada/
def get_map_link(soup):
    address = soup.find(itemprop = 'address').get_text()
    return 'https://www.google.com/maps/search/' + address.replace(' ', '+')


fields = [
    {
        "name": "AD ID",
        "get": lambda soup: soup.find(class_ = 'adId-4111206830').get_text(),
    },
    # {
    #     "name": "City",
    #     "get": lambda soup, _: soup.find(class_ = 'text-2356681840').get_text(),
    # },
    {
        "name": "Contact",
        "URL": True,
        "get": lambda soup: soup.find(class_ = 'link-1956053651').get('href'),
    },
    {
        "name": "For Rent By",
        "get": lambda soup: soup.find(class_ = 'line-2791721720').get_text(),
    },
    {
        "name": "URL",
        #gets updated in scrape_listing
        "get": lambda soup: None,
    },
    {
        "name": "Ad Name",
        "get": lambda soup: soup.find(class_ = 'title-2323565163').get_text(),
    },
    {
        "name": "Map Link",
        "get": get_map_link,
    },
    {
        "name": "Date Posted",
        "get": lambda soup: (soup.select_one('div time') or soup.select_one('div.datePosted-383942873 > span'))['title']
    },
    
    {
        "name": "Unit Type",
        "get": lambda soup: soup(class_ = 'noLabelValue-3861810455')[0].get_text()
    },
    {
        "name": "Bedrooms",
        "get": lambda soup: soup(class_ = 'noLabelValue-3861810455')[1].get_text().split(':')[-1]
    },
    {
        "name": "Bathrooms",
        "get": lambda soup: soup(class_ = 'noLabelValue-3861810455')[2].get_text().split(':')[-1]
    },
    {
        "name": "Featured",
        "get": lambda soup: map_yes_no((soup.find(class_ = 'feature-14975342')))
    },
    {
        "name": "Rent",
        "get": lambda soup: soup.select_one('div.priceWrapper-1165431705 span').get_text()
    },
    {
        "name": "Description",
        "get": lambda soup: soup.select_one('div.descriptionContainer-3261352004 div').get_text('\n')
    },
    {
        "name": "Utilities included",
        "get": lambda soup: '\n'.join([i.get_text() for i in soup.select('.withIcons-3096684796.available-731611581')])
    },
    {
        "name": "Photos", 
        "get": lambda soup: map_yes_no(soup.find(class_ = 'generalOverlay-3042614009')),
        "errorVal": "No"
    },

] + [
    {"name": field_name, "get": lambda soup, field_name = field_name: additional_field_get(soup, field_name)} for field_name in additional_field_names
]

#apply decorator for error checking, decorator for adding base URL
for element in fields:
    if element.get('URL'):
        element['get'] = concat_base_url(element['get'])
    
    element['get'] = error_decorator(element['get'], element.get('errorVal', ERROR_VAL))

field_names = [field['name'] for field in fields]

if __name__ == '__main__': import main
