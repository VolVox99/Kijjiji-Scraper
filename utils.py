from requests.exceptions import ChunkedEncodingError
from time import sleep
from datetime import datetime

def write_to_file(html, filename = 'out'):
    with open(filename + '.html', 'w', encoding = html.encoding) as f: f.write(html.content.decode(html.encoding))

def is_blocked(soup):
    return soup.title == None

def get_req(sesh, url, headers):
    try:
        with sesh.get(url, headers = headers) as req:
            html = req.text
    except ChunkedEncodingError:
        sleep(5)
        return get_req(sesh, url, headers)        
        
    return html


#ex: '8/12/2005
def parse_date_1(date):
    return datetime.strptime(date, "%m/%d/%Y")


#ex: 'September 1, 2021'
def parse_date_2(date):
    return datetime.strptime(date, "%B %d, %Y")

#ex: 'August 4, 2021 12:09 AM'
def parse_date_3(date):
    return datetime.strptime(date, "%B %d, %Y %I:%M %p")
    